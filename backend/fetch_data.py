import yfinance as yf
import csv
import sqlite3
from db_setup import create_database  # Import the database setup function
from indicators.calculate import calculate_ebitda_percentage
from formatters import format_price, format_pe_ratio, format_number


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
            "price": format_price(info.get("currentPrice")),  # Format price
            "pe_ratio": format_pe_ratio(info.get("forwardPE")),  # Format P/E ratio
            "earnings_per_share": format_price(info.get("trailingEps")),  # Format EPS as price
            "revenue": format_number(revenue),  # Format revenue
            "ebitda": calculate_ebitda_percentage(ebitda, revenue),  # Format EBITDA as percentage
        }
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return {
            "ticker": ticker,
            "name": "N/A",
            "price": "N/A",
            "pe_ratio": "N/A",
            "earnings_per_share": "N/A",
            "revenue": "N/A",
            "ebitda": "N/A",
        }


def fetch_all_data(tickers):
    all_data = []
    for ticker in tickers:
        data = fetch_financial_data(ticker)
        if data:
            all_data.append(data)
    return all_data


def save_to_sqlite(data, db_name="data/financial_data.db", tickers=None):
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
            # Apply formatting before saving
            formatted_entry = {
                "ticker": entry["ticker"],
                "name": entry["name"] or "N/A",
                "price": format_price(entry["price"]),
                "pe_ratio": format_pe_ratio(entry["pe_ratio"]),
                "earnings_per_share": format_price(entry["earnings_per_share"]),  # Format EPS as price
                "revenue": format_number(entry["revenue"]),
                "ebitda": calculate_ebitda_percentage(entry["ebitda"], entry["revenue"]),
            }

            cursor.execute('''
                INSERT OR REPLACE INTO financial_data (
                    ticker, name, price, pe_ratio, earnings_per_share, revenue, ebitda
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                formatted_entry["ticker"],
                formatted_entry["name"],
                formatted_entry["price"],
                formatted_entry["pe_ratio"],
                formatted_entry["earnings_per_share"],
                formatted_entry["revenue"],
                formatted_entry["ebitda"],
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
        save_to_sqlite(data, tickers=tickers)
    else:
        print("No tickers found in the file.")


