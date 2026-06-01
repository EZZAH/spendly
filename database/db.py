import sqlite3
from flask import current_app
from werkzeug.security import generate_password_hash


def get_db():
    db_path = current_app.config.get("DATABASE", "spendly.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT NOT NULL,
            email           TEXT UNIQUE NOT NULL,
            password_hash   TEXT NOT NULL,
            created_at      TEXT DEFAULT (datetime('now'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER NOT NULL REFERENCES users(id),
            amount          REAL NOT NULL,
            category        TEXT NOT NULL,
            date            TEXT NOT NULL,
            description     TEXT,
            created_at      TEXT DEFAULT (datetime('now'))
        )
    """)

    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as count FROM users")
    count = cursor.fetchone()["count"]

    if count > 0:
        conn.close()
        return

    password_hash = generate_password_hash("demo123")
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash)
    )

    user_id = cursor.lastrowid

    expenses = [
        (user_id, 500.00, "Food", "2026-05-01", "Grocery shopping"),
        (user_id, 150.00, "Transport", "2026-05-02", "Uber rides"),
        (user_id, 2000.00, "Bills", "2026-05-03", "Electricity bill"),
        (user_id, 300.00, "Health", "2026-05-05", "Pharmacy"),
        (user_id, 800.00, "Entertainment", "2026-05-07", "Movie tickets and dinner"),
        (user_id, 1200.00, "Shopping", "2026-05-10", "Clothing"),
        (user_id, 450.00, "Food", "2026-05-15", "Restaurant"),
        (user_id, 100.00, "Other", "2026-05-20", "Miscellaneous"),
    ]

    cursor.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses
    )

    conn.commit()
    conn.close()
