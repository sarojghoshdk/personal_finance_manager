import os
import sqlite3

# Ensure the 'db' directory exists
os.makedirs("db", exist_ok=True)

def initialize_database():
    conn = sqlite3.connect('db/finance_manager.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        hashed_password TEXT NOT NULL)''')

    # Create transactions table
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        amount REAL,
                        category TEXT,
                        date TEXT,
                        type TEXT,
                        FOREIGN KEY (user_id) REFERENCES users (id))''')

    # Create budgets table
    cursor.execute('''CREATE TABLE IF NOT EXISTS budgets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        category TEXT,
                        amount REAL,
                        FOREIGN KEY (user_id) REFERENCES users (id))''')

    conn.commit()
    conn.close()
    print("Database and tables created successfully.")

if __name__ == "__main__":
    initialize_database()
