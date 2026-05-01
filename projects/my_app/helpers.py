# helpers.py
import sqlite3

DB_PATH = "library.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT,
            year INTEGER,
            publisher TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_books():
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(book) for book in books]

def add_book(title, author, isbn="", year=0, publisher=""):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (title, author, isbn, year, publisher) VALUES (?, ?, ?, ?, ?)",
        (title, author, isbn, year, publisher)
    )
    conn.commit()
    book_id = cursor.lastrowid
    conn.close()
    return {"id": book_id, "title": title, "author": author}

def delete_book(book_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    return True
