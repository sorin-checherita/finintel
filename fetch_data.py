import yfinance as yf
import csv
import sqlite3
from db_setup import create_database  # Import the database setup function


def load_tickers_from_csv(filename="tickers.csv"):
    tickers = []
    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                tickers.append(row[0].strip())
    return tickers


def fetch_financial_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            "ticker": ticker,
            "name": info.get("shortName"),
            "price": info.get("currentPrice"),
            "pe_ratio": info.get("forwardPE"),
            "earnings_per_share": info.get("trailingEps"),
            "revenue": info.get("totalRevenue"),
            "ebitda": info.get("ebitda"),
        }
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None


def fetch_all_data(tickers):
    all_data = []
    for ticker in tickers:
        data = fetch_financial_data(ticker)
        if data:
            all_data.append(data)
    return all_data


def save_to_sqlite(data, db_name="financial_data.db"):
    """
    Save financial data to an SQLite database.

    Args:
        data (list): List of dictionaries containing financial data.
        db_name (str): Name of the SQLite database file.
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Insert data into the table
        for entry in data:
            cursor.execute('''
                INSERT OR REPLACE INTO financial_data (
                    ticker, name, price, pe_ratio, earnings_per_share, revenue, ebitda
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                entry["ticker"],
                entry["name"],
                entry["price"],
                entry["pe_ratio"],
                entry["earnings_per_share"],
                entry["revenue"],
                entry["ebitda"],
            ))

        conn.commit()
        print(f"Data successfully saved to {db_name}")
    except Exception as e:
        print(f"Error saving data to SQLite: {e}")
    finally:
        conn.close()


# Example usage
if __name__ == "__main__":
    # Ensure the database and table are created
    create_database()

    # Load tickers and fetch data
    tickers = load_tickers_from_csv("tickers.csv")
    if tickers:
        data = fetch_all_data(tickers)
        save_to_sqlite(data)
    else:
        print("No tickers found in the file.")


