
# Cloud-Based Bus Pass System

A beginner-friendly internship project built with Python, Flask, SQLite, HTML and CSS.

## Features
- Online bus-pass booking form
- Route-based demo price estimate
- One Day, Weekly and Monthly pass options
- Unique booking reference for every booking
- SQLite database for booking records
- Booking confirmation page
- Demo bookings page at `/admin/bookings`
- Health endpoint at `/health`
- Cloud deployment support using Render

## Technologies Used
- Python
- Flask
- SQLite
- HTML
- CSS
- GitHub
- Render

## Run Locally
1. Install Python 3.10 or later.
2. Open the project folder in VS Code.
3. Open the terminal.
4. Install dependencies:

   `pip install -r requirements.txt`

5. Start the application:

   `python app.py`

6. Open http://127.0.0.1:5000 in your browser.

## Deploy on Render
1. Upload this project to GitHub.
2. Sign in to Render.
3. Choose New + and create a Blueprint or Web Service.
4. Connect the GitHub repository.
5. Use `pip install -r requirements.txt` as the build command.
6. Use `gunicorn app:app` as the start command.
7. Deploy and open the generated public URL.

Persistent storage configuration may require a paid Render plan.

## Important Note
This is an educational demo project. It does not process payments or connect to real bus operators. The admin bookings page has no login protection, so do not enter real or sensitive personal information. Add authentication and security controls before real-world use.
