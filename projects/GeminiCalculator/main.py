import streamlit as st

st.title('GeminiCalculator')

# Input for numbers
num1 = st.number_input("Enter first number", value=0.0, format="%.2f")
num2 = st.number_input("Enter second number", value=0.0, format="%.2f")

# Operation selection
operation = st.selectbox(
    "Select operation",
    ('Add', 'Subtract', 'Multiply', 'Divide')
)

result = None

# Calculate button
if st.button("Calculate"):
    if operation == 'Add':
        result = num1 + num2
    elif operation == 'Subtract':
        result = num1 - num2
    elif operation == 'Multiply':
        result = num1 * num2
    elif operation == 'Divide':
        if num2 != 0:
            result = num1 / num2
        else:
            st.error("Error: Cannot divide by zero!")
            result = None # Ensure result is not shown if error

# Display result
if result is not None:
    st.success(f"Result: {result}")