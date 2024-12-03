from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import sqlite3
from datetime import datetime, timedelta

app = FastAPI()

# CORS Configuration
origins = [
    "http://127.0.0.1:5500",  # Live Server
    "http://127.0.0.1:8000",  # FastAPI
    "http://localhost:5173",  # Vite dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Database setup
con = sqlite3.connect("bootcamp.db")
myCursor = con.cursor()
myCursor.execute("CREATE TABLE IF NOT EXISTS information(date, slideshow, homework_form)")

# Inserting lecture and homework data
start_date = datetime(2024, 9, 24)
end_date = datetime(2024, 11, 26)

while start_date <= end_date:
    date_str = start_date.strftime("%Y-%m-%d")
    match date_str:
        case "2024-09-24":
            slideshow_link = "https://docs.google.com/presentation/d/1VP9mrEZJZ9ALk2dBwadcGkWBg5twjUbM6VFZ7Fn3Vkk/edit?usp=sharing"
            homework_form = None
        case "2024-10-01":
            slideshow_link = "https://docs.google.com/presentation/d/1wO047LhrT73QIcC5WzFhzGOtYhxap3aPq-nYbjmOSKk/edit?usp=sharing"
            homework_form = "https://forms.gle/FtfsBKiXwcuTmXLw7"
        case "2024-10-08":
            slideshow_link = "https://docs.google.com/presentation/d/1RWvO8TQ_ueJyBdSHfZ6oNvq9E6J3rYovItbX_Q-r-44/edit?usp=sharing"
            homework_form = "https://forms.gle/3dnG8S4NUtckh5zD6"
        case "2024-10-15":
            slideshow_link = "https://docs.google.com/presentation/d/14ooPTPyM4QZPWMBq2sg4NypMQZAHQ4rY5n6CUn6l7zI/edit?usp=sharing"
            homework_form = "https://forms.gle/BiJU8QxU1NA43k9d6"
        case "2024-10-22":
            slideshow_link = "https://docs.google.com/presentation/d/1YzEswdGs5zqZMaK8zPCaJl8PiiFFOYDnz2QVHLDAxak/edit?usp=sharing"
            homework_form = "https://forms.gle/LhLmh41u5ckfJdGL7"
                               
        case "2024-10-29":
            slideshow_link = "https://docs.google.com/presentation/d/1GTiIFoT1EDLZ0Y9SC6G1f9c1-YZoMM-NMLOC8-0_-lI/edit?usp=sharing"
            homework_form = "https://forms.gle/8SXRVwGs4q2MQHJD6"
        case "2024-11-05":
            slideshow_link = "https://docs.google.com/presentation/d/15Na7t8cIfSIBrwDEqQ7BOuvSB5UykhBfiqQstg7lqsg/edit?usp=sharing"
            homework_form = "https://forms.gle/8SXRVwGs4q2MQHJD6"
        case "2024-11-12":
            slideshow_link = "https://docs.google.com/presentation/d/1LqK53V6loCTSSouDKSLi0ghzEUEeoyfh49JIIpD04OQ/edit?usp=sharing"
            homework_form = None
        case "2024-11-19" | "2024-11-26":
            slideshow_link = "https://docs.google.com/presentation/d/1l67FCwXIndPk7by-60jXrStApbmZtccyJQhMuFQl4-c/edit?usp=sharing"
            homework_form = None
        case _:
            slideshow_link = ""
            homework_form = ""

    myCursor.execute(
        "INSERT OR REPLACE INTO information (date, slideshow, homework_form) VALUES (?, ?, ?)",
        (date_str, slideshow_link, homework_form),
    )
    start_date += timedelta(weeks=1)

# Commit changes to the database
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
        return {
            "slideshow_link": slideshow,
            "homework_form_link": homework_form or None
        }
    else:
        return {"error": f"No data found for {closest_tuesday_str}. Choose a date between 9/24/2024 and 11/26/2024."}
