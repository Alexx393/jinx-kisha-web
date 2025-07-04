import sqlite3
import os
import datetime

from core.config import get_config

# Load path dynamically so you never hard-code it
CONFIG = get_config()
MEMORY_DB_PATH = CONFIG["memory"]["path"]

# Ensure DB exists
def _init_db():
    if not os.path.exists(MEMORY_DB_PATH):
        conn = sqlite3.connect(MEMORY_DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

_init_db()


def save_interaction(user_input: str, kisha_reply: str):
    conn = sqlite3.connect(MEMORY_DB_PATH)
    c = conn.cursor()
    # Save user input
    c.execute("INSERT INTO memory (role, message) VALUES (?, ?)", ('user', user_input))
    # Save Kisha response
    c.execute("INSERT INTO memory (role, message) VALUES (?, ?)", ('kisha', kisha_reply))
    conn.commit()
    conn.close()


def get_recent_context(limit: int = 10) -> str:
    conn = sqlite3.connect(MEMORY_DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role, message FROM memory ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    rows.reverse()
    return "\n".join([f"{role.capitalize()}: {msg}" for role, msg in rows])


def clear_memory():
    conn = sqlite3.connect(MEMORY_DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM memory")
    conn.commit()
    conn.close()


def search_memory(keyword: str, limit: int = 5) -> list:
    conn = sqlite3.connect(MEMORY_DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT message FROM memory WHERE message LIKE ? ORDER BY id DESC LIMIT ?",
        (f"%{keyword}%", limit)
    )
    results = [row[0] for row in c.fetchall()]
    conn.close()
    return results
