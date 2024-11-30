from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import sqlite3

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
myCursor.execute("CREATE TABLE IF NOT EXISTS information(month, date, year, slideshow link, homework form)")

@app.get("/api/hw/{date}")
def returnHomeworkAssignments(date: str):
    
    #HERE RETURN THE RESPECTIVE HW ASSIGNMENT BASED ON THE PASSED IN DATE
    return {"message": date}

