from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import sqlite3
from datetime import datetime, timedelta

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",  # Add your frontend's URL here
    "http://127.0.0.1:8000",  # Optionally, you can allow localhost itself
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,#origins,  # Allows all origins in the list
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

#creates database if it doesn't already exist
con = sqlite3.connect("bootcamp.db")
myCursor = con.cursor()

#creates table of dates and links if it doesn't exist already
myCursor.execute("CREATE TABLE IF NOT EXISTS information(date, slideshow, homework_form)")

# inserting the data for lectures and homeworks in the databases
# makes it easier for abstraction
# this bootcamp cycle: start date: 2024-9-24 to 2024-11-26
start_date = datetime(2024, 9, 24)
end_date = datetime(2024, 11, 26)

while start_date <= end_date:
    date_str = start_date.strftime("%Y-%m-%d")
    match date_str:
        case "2024-09-24":
            slideshow_link = f"https://docs.google.com/presentation/d/1VP9mrEZJZ9ALk2dBwadcGkWBg5twjUbM6VFZ7Fn3Vkk/edit?usp=sharing"
            homework_form = f"There was no homework this week!"
        case "2024-10-01":
            slideshow_link = f"https://docs.google.com/presentation/d/1wO047LhrT73QIcC5WzFhzGOtYhxap3aPq-nYbjmOSKk/edit?usp=sharing"
            homework_form = f"Git resource link: https://docs.google.com/document/d/1XvymKLdQCiDeWsdRE5CedRp_Gqz25_FeCWCp7qYvrBo/edit?usp=sharing
                              \nHomework Submit form: https://forms.gle/FtfsBKiXwcuTmXLw7"
        case "2024-10-08":
            slideshow_link = f"https://docs.google.com/presentation/d/1RWvO8TQ_ueJyBdSHfZ6oNvq9E6J3rYovItbX_Q-r-44/edit?usp=sharing"
            homework_form = f"Homework Submit form: https://forms.gle/3dnG8S4NUtckh5zD6"
        case "2024-10-15":
            slideshow_link = f"https://docs.google.com/presentation/d/14ooPTPyM4QZPWMBq2sg4NypMQZAHQ4rY5n6CUn6l7zI/edit?usp=sharing"
            homework_form = f"Download Node.js here: https://nodejs.org/en/download/package-manager
                              \nHomework Submit form: https://forms.gle/BiJU8QxU1NA43k9d6"
        case "2024-10-22":
            slideshow_link = f"https://docs.google.com/presentation/d/1YzEswdGs5zqZMaK8zPCaJl8PiiFFOYDnz2QVHLDAxak/edit?usp=sharing"
            homework_form = f"Homework Submit form: 
                              \nReact: https://forms.gle/LhLmh41u5ckfJdGL7
                              \nJS Matching Game: https://forms.gle/SikXYsLiDJnQCgr28"
        case "2024-10-29":
            slideshow_link = f"https://docs.google.com/presentation/d/1GTiIFoT1EDLZ0Y9SC6G1f9c1-YZoMM-NMLOC8-0_-lI/edit?usp=sharing"
            homework_form = f"Homework Submit form: https://forms.gle/8SXRVwGs4q2MQHJD6"
        case "2024-11-05":
            slideshow_link = f"https://docs.google.com/presentation/d/15Na7t8cIfSIBrwDEqQ7BOuvSB5UykhBfiqQstg7lqsg/edit?usp=sharing"
            homework_form = f"Extended Twitter HW! Submit here: https://forms.gle/8SXRVwGs4q2MQHJD6
                              \nVideo to watch: https://youtu.be/fWjsdhR3z3c?si=tTJMWE6hhdmI0Vnk"
        case "2024-11-12":
            slideshow_link = f"https://docs.google.com/presentation/d/1LqK53V6loCTSSouDKSLi0ghzEUEeoyfh49JIIpD04OQ/edit?usp=sharing"
            homework_form = f"No homework, only the hackathon!" 
        case "2024-11-19":
            slideshow_link = f"https://docs.google.com/presentation/d/1l67FCwXIndPk7by-60jXrStApbmZtccyJQhMuFQl4-c/edit?usp=sharing"
            homework_form = f"No homework, only the hackathon!"
        case "2024-11-26":
            slideshow_link = f"https://docs.google.com/presentation/d/1l67FCwXIndPk7by-60jXrStApbmZtccyJQhMuFQl4-c/edit?usp=sharing"
            homework_form = f"No homework, only the hackathon!"
        case _:
            slideshow_link = f""
            homework_form = f""
    
    myCursor.execute("INSERT OR REPLACE INTO information (date, slideshow, homework_form) VALUES (?, ?, ?)",
                     (date_str, slideshow_link, homework_form))
    
    # moving the date to next tuesday 
    start_date += timedelta(weeks = 1)

# Committing the changes to the database
con.commit()

@app.get("/{date}")
def returnHomeworksAndLectures(date: str):
    
    # convert date string into something more manageable
    try:
        date_fmt = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Please use YYYY-MM-DD."}

    # find the closest previous tuesday (if the date is not a Tuesday)
    days_to_tuesday = (date_fmt.weekday() - 1) % 7  # number of days back to the prev Tuesday
    closest_tuesday = date_fmt - timedelta(days=days_to_tuesday)

    # Convert back to formatted string in this YYYY-MM-DD format (aka the format we called stuff)
    closest_tuesday_str = closest_tuesday.strftime("%Y-%m-%d")

    # getting the homework and lec links from the closest (latest) tuesday
    con = sqlite3.connect("bootcamp.db")
    myCursor = con.cursor()
    myCursor.execute("SELECT slideshow, homework_form FROM information WHERE date = ?", (closest_tuesday_str,))
    
    result = myCursor.fetchone()

    if result:
        slideshow, homework_form = result
        #HERE RETURN THE RESPECTIVE HW ASSIGNMENT BASED ON THE PASSED IN DATE
        return {"slideshow_link": slideshow, "homework_form_link": homework_form}
    else:
        return {"error": f"No data found for {closest_tuesday_str}. Choose a date between 9/24/2024 and 11/26/2024."}

