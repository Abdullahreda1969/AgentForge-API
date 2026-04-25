# core/templates.py
"""قوالب موحدة - تستخدمها جميع الوكلاء في كلا الوضعين"""

class Templates:
    
    @staticmethod
    def config():
        return '''# config.py
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
APP_NAME = "My Application"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
'''
    
    @staticmethod
    def get_database_template():
        """قالب database.py - SQLite (تخزين دائم)"""
        
        return '''# database.py
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
'''
        
    @staticmethod
    def get_helpers_template(project_type, item_name):
        """قالب helpers.py - SQLite (تخزين دائم)"""
        
        items_name = f"{item_name}s"
        
        return f'''# helpers.py
from database import get_all_items, get_item_by_id, add_item, update_item, delete_item

def get_{items_name}():
    """جلب جميع {items_name}"""
    return get_all_items()

def get_{item_name}({item_name}_id):
    """جلب {item_name} محدد"""
    return get_item_by_id({item_name}_id)

def add_{item_name}(name: str, description: str = ""):
    """إضافة {item_name} جديد"""
    return add_item(name=name, description=description)

def update_{item_name}({item_name}_id: int, **kwargs):
    """تحديث {item_name}"""
    return update_item({item_name}_id, **kwargs)

def delete_{item_name}({item_name}_id):
    """حذف {item_name}"""
    return delete_item({item_name}_id)
'''
    
    @staticmethod
    def main(project_type, item_name):
        items_name = f"{item_name}s"
        titles = {"task": "📝 Task Manager", "contact": "📞 Contact Book", "product": "📦 Inventory"}
        title = titles.get(project_type, f"📱 {item_name.title()} Manager")
        
        return f'''# main.py
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from helpers import get_{items_name}, add_{item_name}, delete_{item_name}

st.set_page_config(page_title="{title}", layout="wide")
st.title("{title}")

with st.sidebar:
    st.header("Add New")
    with st.form("add_form"):
        name = st.text_input("Name")
        description = st.text_area("Description")
        if st.form_submit_button("Add"):
            add_{item_name}(name=name, description=description)
            st.rerun()

st.header(f"{items_name.title()} List")
items = get_{items_name}()

if not items:
    st.info("No items yet. Add one from the sidebar!")
else:
    for item in items:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{{item.get('name')}}**")
            if item.get("description"):
                st.caption(item.get("description"))
        with col2:
            if st.button("Delete", key=item.get("id")):
                delete_{item_name}(item.get("id"))
                st.rerun()

st.caption("Powered by AgentForge")
'''
    
    @staticmethod
    def start_bat():
        return '@echo off\nstreamlit run main.py\npause'
    
    @staticmethod
    def detect_type(description):
        desc = description.lower()
        if any(w in desc for w in ['contact', 'address', 'phone', 'جهة', 'عنوان', 'دفتر']):
            return "contact", "contact"
        if any(w in desc for w in ['task', 'todo', 'reminder', 'مهمة', 'مهام', 'تذكير']):
            return "task", "task"
        if any(w in desc for w in ['product', 'inventory', 'منتج', 'مخزون']):
            return "product", "product"
        return "general", "item"