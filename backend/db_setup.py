def create_database(db_name="data/financial_data.db"):
    """
    Create the SQLite database and the required tables.

    Args:
        db_name (str): Name of the SQLite database file.
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Create the financial_data table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS financial_data (
                ticker TEXT PRIMARY KEY,
                name TEXT,
                price REAL,
                pe_ratio REAL,
                earnings_per_share REAL,
                revenue REAL,
                ebitda REAL
            )
        ''')

        conn.commit()
        print(f"Database and table successfully created in {db_name}")
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    create_database()