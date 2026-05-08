import streamlit as st
import helpers

st.title('TinyTest')

# Calculator
if st.button('Calculator'):
    with st.sidebar:
        calculator_result = helpers.calculate()
        st.write(f'Result: {calculator_result}')

# Blog
if st.button('Blog'):
    st.title('My Blog')
    post1 = st.container()
    post1.write('Post 1 Title
This is the content of post 1.')
    post2 = st.container()
    post2.write('Post 2 Title
This is the content of post 2.')

# Contact Book
if st.button('Contact Book'):
    st.title('Contact Book')
    contact1 = st.container()
    contact1.write('Name: John Doe
Phone: 123-456-7890
Email: john.doe@example.com')
    contact2 = st.container()
    contact2.write('Name: Jane Smith
Phone: 987-654-3210
Email: jane.smith@example.com')