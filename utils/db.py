# utils/db.py
import sqlite3
import os

DB_PATH = "data/history/history.db"

# Ensure DB is initialized
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            prediction TEXT,
            confidence REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Save prediction to history
def save_history(filename, prediction, confidence):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO history (filename, prediction, confidence) VALUES (?, ?, ?)',
              (filename, prediction, confidence))
    conn.commit()
    conn.close()

# Load history
def load_history():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT filename, prediction, confidence, timestamp FROM history ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    return rows

# utils/db.py
def clear_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='history'")  # reset ID count
    conn.commit()
    conn.close()