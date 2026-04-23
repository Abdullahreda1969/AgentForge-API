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
    def database():
        return '''# database.py
# Simple in-memory storage (no SQLAlchemy)
_items = []
_next_id = 1

def get_all():
    return _items

def add(item_data):
    global _next_id
    item_data["id"] = _next_id
    _items.append(item_data)
    _next_id += 1
    return item_data

def delete(item_id):
    global _items
    _items = [i for i in _items if i.get("id") != item_id]
    return True
'''
    
    @staticmethod
    def helpers(project_type, item_name):
        items_name = f"{item_name}s"
        return f'''# helpers.py
_items = []
_next_id = 1

def get_{items_name}():
    return _items

def get_{item_name}({item_name}_id):
    for item in _items:
        if item.get("id") == {item_name}_id:
            return item
    return None

def add_{item_name}(name: str, description: str = ""):
    global _next_id
    item = {{"id": _next_id, "name": name, "description": description}}
    _items.append(item)
    _next_id += 1
    return item

def delete_{item_name}({item_name}_id):
    global _items
    _items = [i for i in _items if i.get("id") != {item_name}_id]
    return True
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