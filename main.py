'''Install the required libraries'''

from fastapi import FastAPI
from app.schemas import TextData
from transformers import pipeline
from datetime import datetime
import sqlite3
import os

app = FastAPI(title="NLP MLOps System")

# LLM model
classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

DB_PATH = "/logs.db" #Create a file to store recent data

def init_db():
    os.makedirs("/data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH) #Database connection
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            text TEXT,
            prediction TEXT,
            confidence REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

'''Creating the expected endpoint'''

@app.post("/predict")
def predict(data: TextData):
    result = classifier(data.text)[0]

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
  '''Data storage in the file'''
    c.execute("""
        INSERT INTO logs VALUES (?, ?, ?, ?)
    """, (
        data.text,
        result["label"],
        result["score"],
        str(datetime.now())
    ))
    conn.commit()
    conn.close()

    return {"result": result} #return the result
