import yfinance as yf
import csv
import sqlite3
from backend.db_setup import create_database  # Import the database setup function
from backend.indicators.calculate import calculate_ebitda_percentage
from backend.utils.formatters import format_price, format_pe_ratio, format_number


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

        ebitda = info.get("ebitda")
        revenue = info.get("totalRevenue")

        return {
            "ticker": ticker,
            "name": info.get("shortName") or "N/A",
            "price": info.get("currentPrice"),
            "pe_ratio": info.get("forwardPE"),
            "earnings_per_share": info.get("trailingEps"),
            "revenue": revenue,
            "ebitda": ebitda,
        }
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return {
            "ticker": ticker,
            "name": "N/A",
            "price": None,
            "pe_ratio": None,
            "earnings_per_share": None,
            "revenue": None,
            "ebitda": None,
        }


def fetch_all_data(tickers):
    all_data = []
    for ticker in tickers:
        data = fetch_financial_data(ticker)
        if data:
            all_data.append(data)
    return all_data


def save_to_sqlite(data, db_name="database/financial_data.db", tickers=None):
    """
    Save financial data to an SQLite database and remove outdated tickers.

    Args:
        data (list): List of dictionaries containing financial data.
        db_name (str): Name of the SQLite database file.
        tickers (list): List of tickers currently in the CSV file.
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Remove outdated tickers from the database
        if tickers:
            cursor.execute("DELETE FROM financial_data WHERE ticker NOT IN ({})".format(
                ",".join("?" for _ in tickers)
            ), tickers)

        # Insert or update data for the current tickers
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


def add_ticker_to_database(ticker, db_name="database/financial_data.db"):
    """
     Fetch financial data for a ticker and save it to the database.

    Args:
        ticker (str): The ticker symbol to add.
        db_name (str): The name of the SQLite database file.

    Returns:
        dict: The financial data for the ticker.
    """
    try:
        # Fetch financial data for the ticker
        financial_data = fetch_financial_data(ticker)
        if not financial_data:
            raise ValueError(f"Could not fetch data for ticker: {ticker}")
        
        # Save to database
        save_to_sqlite([financial_data], db_name=db_name)
        print(f"Ticker {ticker} added to database with data: {financial_data}")
        return financial_data
    
    except Exception as e:
        print(f"Error adding ticker {ticker} to database: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # Ensure the database and table are created
    create_database()

    # Load tickers and fetch data
    tickers = load_tickers_from_csv("tickers.csv")
    if tickers:
        data = fetch_all_data(tickers)
        save_to_sqlite(data, tickers=tickers)
    else:
        print("No tickers found in the file.")


