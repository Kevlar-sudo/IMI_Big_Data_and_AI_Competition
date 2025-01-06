import sqlite3
import os

DB_NAME = 'mydatabase.db'

def init_db():
    """Initialize the SQLite database if it doesn't already exist."""
    # Check if the DB file exists
    db_exists = os.path.exists(DB_NAME)

    # Connect to (or create) the SQLite database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    if not db_exists:
        # Create a table named 'items'
        c.execute('''
            CREATE TABLE items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        conn.commit()

    # Always close your connections
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized!")