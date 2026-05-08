import sqlite3

def create_tables():
    """Creates the necessary tables in the database."""
    conn = sqlite3.connect('tinytest.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS calculator_results ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                result TEXT
                )''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()