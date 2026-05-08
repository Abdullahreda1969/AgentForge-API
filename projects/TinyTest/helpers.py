def calculate():
    """Performs basic calculations."""
    num1 = float(st.number_input('Enter first number', value=0.0))
    operator = st.selectbox('Select operator', ['+', '-', '*', '/'])
    num2 = float(st.number_input('Enter second number', value=0.0))

    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    elif operator == '*':
        result = num1 * num2
    elif operator == '/':
        if num2 == 0:
            return 'Error: Division by zero!'
        result = num1 / num2
    else:
        return 'Invalid operator!'

    return result