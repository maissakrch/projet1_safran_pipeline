from fastapi import FastAPI
import sqlite3
import pandas as pd
from logger import log


app = FastAPI(title="Safran Data Pipeline API")

DB_PATH = "data/final.db"

def query_db(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

@app.get("/")
def root():
    return {"message": "API du pipeline Safran opérationnelle"}

@app.get("/mesures")
def get_all_mesures(limit: int = 100):
    df = query_db(f"SELECT * FROM mesures LIMIT {limit}")
    return df.to_dict(orient="records")

@app.get("/mesures/{unit_id}")
def get_mesures_by_unit(unit_id: int):
    df = query_db(f"SELECT * FROM mesures WHERE unit = {unit_id}")
    return df.to_dict(orient="records")
