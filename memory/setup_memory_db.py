# memory/setup_memory_db.py

import sqlite3
import os
from core.config import get_config

CONFIG = get_config()
MEMORY_DB_PATH = CONFIG["memory"]["path"]

def init_memory_table():
    # Ensure parent folder exists
    os.makedirs(os.path.dirname(MEMORY_DB_PATH), exist_ok=True)

    conn = sqlite3.connect(MEMORY_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()
    print(f"🧠 Memory DB initialized at: {MEMORY_DB_PATH}")

if __name__ == "__main__":
    init_memory_table()
