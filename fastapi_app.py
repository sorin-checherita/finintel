from fastapi import FastAPI, HTTPException
from fetch_data import fetch_all_data, load_tickers_from_csv
from db_setup import create_database
import sqlite3

app = FastAPI()

DB_NAME = "financial_data.db"

# Endpoint pentru a obține toate datele financiare din baza de date


@app.get("/financial-data")
def get_financial_data():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM financial_data")
        rows = cursor.fetchall()

        # Structurăm datele într-un format JSON
        data = [
            {
                "ticker": row[0],
                "name": row[1],
                "price": row[2],
                "pe_ratio": row[3],
                "earnings_per_share": row[4],
                "revenue": row[5],
                "ebitda": row[6],
            }
            for row in rows
        ]

        conn.close()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")


# Endpoint pentru a actualiza datele financiare
@app.post("/update-data")
def update_financial_data():
    try:
        # Încarcă tickerele din fișierul CSV
        tickers = load_tickers_from_csv("tickers.csv")
        if not tickers:
            raise HTTPException(status_code=400, detail="No tickers found in tickers.csv")

        # Fetch date financiare pentru tickere
        financial_data = fetch_all_data(tickers)

        # Salvează datele în baza de date
        from fetch_data import save_to_sqlite
        save_to_sqlite(financial_data)

        return {"message": "Financial data updated successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating data: {e}")


# Endpoint pentru a obține datele financiare pentru un ticker specific
@app.get("/financial-data/{ticker}")
def get_ticker_data(ticker: str):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM financial_data WHERE ticker = ?", (ticker,))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail=f"No data found for ticker: {ticker}")

        data = {
            "ticker": row[0],
            "name": row[1],
            "price": row[2],
            "pe_ratio": row[3],
            "earnings_per_share": row[4],
            "revenue": row[5],
            "ebitda": row[6],
        }

        conn.close()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data for ticker: {e}")


# Endpoint pentru a inițializa baza de date
@app.post("/initialize-db")
def initialize_database():
    try:
        create_database()
        return {"message": "Database initialized successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing database: {e}")


# Endpoint pentru a verifica starea aplicației
@app.get("/")
def read_root():
    return {"message": "Welcome to FinIntel API!"}