import os
import pandas as pd
import matplotlib.pyplot as plt
from fastapi.responses import FileResponse
from database.db import UPLOAD_DIR
import pandas as pd
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
from sqlalchemy.orm import Session
from passlib.hash import argon2 
from models.model import  users 
from models.auth import  login_user
from groq import Groq
from database.db import UPLOAD_DIR

from fastapi import FastAPI, UploadFile, File
import mimetypes
app = FastAPI()
import os
from fastapi.responses import FileResponse



def  signup_service(db : Session ,x:str, a:str , b : str , c:str):
    bb = argon2.hash(b)
    user = users(name = x ,email = a , password = bb , role = c)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message" : "you data has been stored , please go to login page"}

def download_file(file_name:str):
    file_path = os.path.join(UPLOAD_DIR,file_name)
    if not file_path:
        return{"msg":"not found"}
    mime_type,_= mimetypes.guess_type(file_path)
    return FileResponse (path = file_path , filename = file_name , media_type = mime_type)



CHART_DIR = "charts"
os.makedirs(CHART_DIR, exist_ok=True)


def view_raw_csv_service(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise Exception("CSV file not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="text/csv"
    )


def generate_chart_service(filename: str, chart_type: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise Exception("CSV file not found")

    df = pd.read_csv(file_path)

    plt.figure()

    if chart_type == "line chart":
        df.plot(kind="line")
    elif chart_type == "area chart":
        df.plot(kind="area")
    elif chart_type == "scatter chart":
        plt.scatter(df.iloc[:, 0], df.iloc[:, 1])
    else:
        raise Exception("Invalid chart type")

    chart_path = os.path.join(CHART_DIR, f"{chart_type}_{filename}.png")
    plt.savefig(chart_path)
    plt.close()

    return chart_path

CSV_PATH = r"F:\PYTHON PROGRAMS\day38\ERP-pending\backend\factory_file.csv"
client = Groq(api_key="gsk")
def ai_search_service(search: str):
    if not search:
        return "Please enter a search term"
    if not os.path.exists(CSV_PATH):
        return "Currently we don't have this file. We will add it soon."
    df = pd.read_csv(CSV_PATH)
    csv_text = df.head(20).to_string(index=False)
    prompt = f"""
Here is our factory CSV data:
{csv_text}
User search input:
{search}
Perform a search on the CSV data and return a short result , keep your message dynamic for each time , even if you don't fine the exact thing you can also print most relevant thing
(10 to 30 words only).
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": prompt}],
        temperature=0
    )
    result = response.choices[0].message.content.strip()
    return result


   