
import os
import sqlite3
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-for-production")

DATA_DIR = os.environ.get("DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "bus_passes.db")

ROUTES = {
    "Ahmedabad to Gandhinagar": 40,
    "Ahmedabad to Sanand": 35,
    "Ahmedabad to Kalol": 45,
    "Ahmedabad to Dholka": 50,
    "Ahmedabad to Nadiad": 70,
}


def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_code TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                route TEXT NOT NULL,
                pass_type TEXT NOT NULL,
                price REAL NOT NULL,
                travel_date TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


@app.route("/")
def index():
    return render_template("index.html", routes=ROUTES)


@app.route("/book", methods=["POST"])
def book():
    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    route = request.form.get("route", "").strip()
    pass_type = request.form.get("pass_type", "").strip()
    travel_date = request.form.get("travel_date", "").strip()

    if not all([full_name, email, phone, route, pass_type, travel_date]):
        flash("Please complete every field.", "error")
        return redirect(url_for("index"))

    if route not in ROUTES or pass_type not in {"One Day", "Weekly", "Monthly"}:
        flash("Please choose a valid route and pass type.", "error")
        return redirect(url_for("index"))

    multiplier = {"One Day": 1, "Weekly": 5, "Monthly": 20}[pass_type]
    price = ROUTES[route] * multiplier
    booking_code = "BUS-" + uuid.uuid4().hex[:8].upper()

    try:
        with get_db() as connection:
            connection.execute("""
                INSERT INTO bookings
                (booking_code, full_name, email, phone, route, pass_type,
                 price, travel_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                booking_code, full_name, email, phone, route,
                pass_type, price, travel_date,
                datetime.utcnow().isoformat(timespec="seconds")
            ))
    except sqlite3.IntegrityError:
        flash("Could not create a unique booking ID. Please try again.", "error")
        return redirect(url_for("index"))

    return redirect(url_for("confirmation", booking_code=booking_code))


@app.route("/confirmation/<booking_code>")
def confirmation(booking_code):
    with get_db() as connection:
        booking = connection.execute(
            "SELECT * FROM bookings WHERE booking_code = ?",
            (booking_code,)
        ).fetchone()

    if booking is None:
        return render_template("not_found.html"), 404

    return render_template("confirmation.html", booking=booking)


@app.route("/admin/bookings")
def admin_bookings():
    # Demo-only route. Add authentication before real use.
    with get_db() as connection:
        bookings = connection.execute(
            "SELECT * FROM bookings ORDER BY id DESC LIMIT 100"
        ).fetchall()

    return render_template("admin.html", bookings=bookings)


@app.route("/health")
def health():
    return {"status": "ok"}


init_db()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
