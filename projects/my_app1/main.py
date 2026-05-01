
# main.py
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from helpers import get_books, add_book, delete_book

st.set_page_config(page_title="📚 Library Manager", layout="wide")
st.title("📚 Library Manager")

with st.sidebar:
    st.header("Add New Book")
    with st.form("add_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        isbn = st.text_input("ISBN (optional)")
        year = st.number_input("Year", min_value=0, max_value=2026, step=1)
        publisher = st.text_input("Publisher (optional)")
        submitted = st.form_submit_button("Add Book")

        if submitted and title and author:
            add_book(title=title, author=author, isbn=isbn, year=year, publisher=publisher)
            st.success(f"Added: {title}")
            st.rerun()

st.header("Books List")
books = get_books()

if not books:
    st.info("No books yet. Add one from the sidebar!")
else:
    for book in books:
        with st.expander(f"📖 {book['title']} - {book['author']}"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**ISBN:** {book.get('isbn', 'N/A')}")
                st.write(f"**Year:** {book.get('year', 'N/A')}")
                st.write(f"**Publisher:** {book.get('publisher', 'N/A')}")
            with col2:
                if st.button("Delete", key=book['id']):
                    delete_book(book['id'])
                    st.rerun()

st.caption("Powered by AgentForge")
