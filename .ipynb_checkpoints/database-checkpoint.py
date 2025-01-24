import sqlite3
import os
import pandas as pd

DB_NAME = 'mydatabase.db'
CSV_FILE_PATH = 'csv_files\eft.csv'  # Update this path if the file is moved
TABLE_NAME = 'items'  # Table name


def init_db(csv_path, db_name, table_name):
    """Initialize the SQLite database and create a table with specified columns."""
    # Desired column names and types
    column_definitions = {
    "eft_id": "TEXT PRIMARY KEY",
    "customer_id": "INTEGER",
    "amount_cad": "REAL",
    "debit_credit": "TEXT",
    "transaction_date": "TEXT",
    "transaction_time": "TEXT",
}

    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Drop the table if it already exists
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    print(f"Existing table '{table_name}' has been dropped.")

    # Create the table with specified schema
    column_definitions_sql = ", ".join([f"{col} {dtype}" for col, dtype in column_definitions.items()])
    create_table_sql = f"CREATE TABLE {table_name} ({column_definitions_sql});"
    print(f"Creating table with SQL: {create_table_sql}")
    cursor.execute(create_table_sql)

    # Commit and close the connection
    conn.commit()
    conn.close()


def load_csv_to_db(csv_path, db_name, table_name):
    """Load data from a CSV file into the SQLite database."""
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_path)

    # Ensure the column names match the desired schema
    expected_columns = ["eft_id", "customer_id", "amount_cad", "debit_credit", "transaction_date", "transaction_time"]
    if not all(col in df.columns for col in expected_columns):
        raise ValueError(f"The CSV file is missing required columns. Expected: {expected_columns}")

    # Reorder columns to match the table schema
    df = df[expected_columns]

    # Connect to the database
    conn = sqlite3.connect(db_name)

    try:
        # Insert the data into the table
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"Data from {csv_path} has been loaded into the table {table_name}.")
    except Exception as e:
        print(f"Error while inserting data: {e}")
    finally:
        # Close the connection
        conn.close()


if __name__ == "__main__":
    # Step 1: Initialize the database and create the table
    init_db(CSV_FILE_PATH, DB_NAME, TABLE_NAME)

    # Step 2: Load CSV data into the database
    load_csv_to_db(CSV_FILE_PATH, DB_NAME, TABLE_NAME)

    print("Database initialized and data loaded!")
