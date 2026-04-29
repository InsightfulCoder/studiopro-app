import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "studiopro.db")

def migrate_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Add credits column if it doesn't exist
        cursor.execute("ALTER TABLE users ADD COLUMN credits INTEGER DEFAULT 0")
        print("Successfully added 'credits' column to 'users' table.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("Column 'credits' already exists. Skipping migration.")
        else:
            print(f"Error during migration: {e}")
    finally:
        conn.commit()
        conn.close()

if __name__ == "__main__":
    migrate_db()
