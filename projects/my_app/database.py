# database.py
import os
import sqlite3
from datetime import datetime
from typing import List, Dict, Any

DB_PATH = os.getenv("DATABASE_PATH", "app.db")

def get_db_connection():
    """إنشاء اتصال بقاعدة البيانات"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """تهيئة قاعدة البيانات وإنشاء الجداول"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

# تهيئة قاعدة البيانات عند بدء التطبيق
init_db()

def get_all_items() -> List[Dict[str, Any]]:
    """جلب جميع العناصر"""
    conn = get_db_connection()
    items = conn.execute("SELECT * FROM items ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(item) for item in items]

def get_item_by_id(item_id: int) -> Dict[str, Any]:
    """جلب عنصر محدد بالمعرف"""
    conn = get_db_connection()
    item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    conn.close()
    return dict(item) if item else None

def add_item(name: str, description: str = "") -> Dict[str, Any]:
    """إضافة عنصر جديد"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name, description) VALUES (?, ?)",
        (name, description)
    )
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return get_item_by_id(item_id)

def update_item(item_id: int, **kwargs) -> bool:
    """تحديث عنصر"""
    conn = get_db_connection()
    updates = ", ".join([f"{key} = ?" for key in kwargs.keys()])
    values = list(kwargs.values()) + [item_id]
    
    conn.execute(f"UPDATE items SET {updates} WHERE id = ?", values)
    conn.commit()
    conn.close()
    return True

def delete_item(item_id: int) -> bool:
    """حذف عنصر"""
    conn = get_db_connection()
    conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return True
