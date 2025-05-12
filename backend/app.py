from fetch_data import load_tickers_from_csv, fetch_all_data, save_to_sqlite
from db_setup import create_database

def main():
    # 1. Creare baza de date și tabel
    create_database()

    # 2. Încărcare tickere din fișier CSV
    tickers = load_tickers_from_csv("tickers.csv")
    if not tickers:
        print("Fișierul tickers.csv este gol sau nu există.")
        return

    # 3. Fetch date financiare pentru tickere
    print("Se obțin datele financiare...")
    financial_data = fetch_all_data(tickers)

    # 4. Salvare date în baza de date SQLite
    print("Se salvează datele în baza de date...")
    save_to_sqlite(financial_data)

    print("Proces finalizat cu succes!")


if __name__ == "__main__":
    main()

