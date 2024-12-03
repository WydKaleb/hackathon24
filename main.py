from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import sqlite3
from datetime import datetime, timedelta

app = FastAPI()

# CORS Configuration
origins = [
    "http://127.0.0.1:5500",  # If you use Live Server
    "http://127.0.0.1:8000",  # Localhost for FastAPI
    "http://localhost:5173",  # Your frontend's origin (Vite dev server)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow these specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Database connection and setup
con = sqlite3.connect("bootcamp.db")
myCursor = con.cursor()
myCursor.execute("CREATE TABLE IF NOT EXISTS information(date, slideshow, homework_form)")

# Sample Data Insertion
start_date = datetime(2024, 9, 24)
end_date = datetime(2024, 11, 26)
while start_date <= end_date:
    date_str = start_date.strftime("%Y-%m-%d")
    match date_str:
        case "2024-09-24":
            slideshow_link = "https://docs.google.com/presentation/d/1VP9mrEZJZ9ALk2dBwadcGkWBg5twjUbM6VFZ7Fn3Vkk/edit?usp=sharing"
            homework_form = "There was no homework this week!"
        case "2024-10-01":
            slideshow_link = "https://docs.google.com/presentation/d/1wO047LhrT73QIcC5WzFhzGOtYhxap3aPq-nYbjmOSKk/edit?usp=sharing"
            homework_form = (
                "Git resource link: https://docs.google.com/document/d/1XvymKLdQCiDeWsdRE5CedRp_Gqz25_FeCWCp7qYvrBo/edit?usp=sharing\n"
                "Homework Submit form: https://forms.gle/FtfsBKiXwcuTmXLw7"
            )
        # Add other dates similarly
        case _:
            slideshow_link = ""
            homework_form = ""

    myCursor.execute("INSERT OR REPLACE INTO information (date, slideshow, homework_form) VALUES (?, ?, ?)",
                     (date_str, slideshow_link, homework_form))
    start_date += timedelta(weeks=1)

con.commit()

@app.get("/{date}")
def returnHomeworksAndLectures(date: str):
    try:
        date_fmt = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Please use YYYY-MM-DD."}

    days_to_tuesday = (date_fmt.weekday() - 1) % 7
    closest_tuesday = date_fmt - timedelta(days=days_to_tuesday)
    closest_tuesday_str = closest_tuesday.strftime("%Y-%m-%d")

    con = sqlite3.connect("bootcamp.db")
    myCursor = con.cursor()
    myCursor.execute("SELECT slideshow, homework_form FROM information WHERE date = ?", (closest_tuesday_str,))
    result = myCursor.fetchone()

    if result:
        slideshow, homework_form = result
        return {"slideshow_link": slideshow, "homework_form_link": homework_form}
    else:
        return {"error": f"No data found for {closest_tuesday_str}. Choose a date between 9/24/2024 and 11/26/2024."}
