
# main.py
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from helpers import get_items, add_item, delete_item

st.set_page_config(page_title="📱 Item Manager", layout="wide")
st.title("📱 Item Manager")

with st.sidebar:
    st.header("Add New")
    with st.form("add_form"):
        name = st.text_input("Name")
        description = st.text_area("Description")
        if st.form_submit_button("Add"):
            add_item(name=name, description=description)
            st.rerun()

st.header(f"Items List")
items = get_items()

if not items:
    st.info("No items yet. Add one from the sidebar!")
else:
    for item in items:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{item.get('name')}**")
            if item.get("description"):
                st.caption(item.get("description"))
        with col2:
            if st.button("Delete", key=item.get("id")):
                delete_item(item.get("id"))
                st.rerun()

st.caption("Powered by AgentForge")
