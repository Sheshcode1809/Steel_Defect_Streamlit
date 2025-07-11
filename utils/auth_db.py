import sqlite3
import hashlib
import os

DB_PATH = "users.db"

# Connect to the SQLite database
def connect_db():
    return sqlite3.connect(DB_PATH)

# Create necessary tables (users and history)
def create_tables():
    conn = connect_db()
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')

    # Create history table
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            username TEXT,
            image TEXT,
            label TEXT,
            confidence REAL
        )
    ''')

    conn.commit()
    conn.close()

# Add a new user (returns True if successful, False if username already exists)
def add_user(username, password):
    conn = connect_db()
    c = conn.cursor()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True
    except Exception as e:
        print(f"[ERROR] add_user: {e}")
        return False
    finally:
        conn.close()

# Validate user login credentials
def validate_user(username, password):
    conn = connect_db()
    c = conn.cursor()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    try:
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
        return c.fetchone() is not None
    except Exception as e:
        print(f"[ERROR] validate_user: {e}")
        return False
    finally:
        conn.close()

# Save a prediction to the history table
def save_user_prediction(username, image, label, confidence):
    conn = connect_db()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO history VALUES (?, ?, ?, ?)", (username, image, label, confidence))
        conn.commit()
    except Exception as e:
        print(f"[ERROR] save_user_prediction: {e}")
    finally:
        conn.close()

# Fetch prediction history for a specific user
def get_user_history(username):
    conn = connect_db()
    c = conn.cursor()
    try:
        c.execute("SELECT image, label, confidence FROM history WHERE username=?", (username,))
        return c.fetchall()
    except Exception as e:
        print(f"[ERROR] get_user_history: {e}")
        return []
    finally:
        conn.close()

def clear_user_history(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("DELETE FROM history WHERE username=?", (username,))
    conn.commit()
    conn.close()
