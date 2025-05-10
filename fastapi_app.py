from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fetch_data import fetch_all_data, load_tickers_from_csv
from db_setup import create_database
from formatters import format_price, format_pe_ratio, format_number
from indicators.calculate import calculate_ebitda_percentage
import sqlite3

app = FastAPI()

DB_NAME = "financial_data.db"

# Mount static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the index.html file at the root path
@app.get("/")
def read_root():
    return FileResponse("static/index.html")

# Endpoint pentru a obține toate datele financiare din baza de date
@app.get("/financial-data")
def get_financial_data():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Fetch raw data from the database
        cursor.execute("SELECT * FROM financial_data")
        rows = cursor.fetchall()

        # Format the data dynamically before returning
        data = [
            {
                "ticker": row[0],
                "name": row[1] or "N/A",
                "price": format_price(row[2]),
                "pe_ratio": format_pe_ratio(row[3]),
                "earnings_per_share": format_price(row[4]),
                "revenue": format_number(row[5]),
                "ebitda": calculate_ebitda_percentage(row[6], row[5]),
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
        # Load tickers from the CSV file
        tickers = load_tickers_from_csv("tickers.csv")
        if not tickers:
            raise HTTPException(status_code=400, detail="No tickers found in tickers.csv")

        # Fetch financial data for the tickers
        financial_data = fetch_all_data(tickers)

        # Save the data to the database and remove outdated tickers
        from fetch_data import save_to_sqlite
        save_to_sqlite(financial_data, db_name=DB_NAME, tickers=tickers)

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