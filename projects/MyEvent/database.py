# database.py
import sqlite3
from config import DATABASE_NAME, EVENTS_TABLE_NAME, EVENTS_COLUMNS, ATTENDEES_TABLE_NAME, ATTENDEES_COLUMNS

def get_db_connection():
    """Establishes a connection to the SQLite database and returns the connection object."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name (e.g., row['column_name'])
    return conn

def create_tables():
    """Creates the 'events' and 'attendees' tables in the database if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Construct SQL for EVENTS table creation
    events_cols_str = ", ".join([f"{col_name} {col_type}" for col_name, col_type in EVENTS_COLUMNS.items()])
    create_events_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {EVENTS_TABLE_NAME} (
        {events_cols_str}
    );
    """
    cursor.execute(create_events_table_sql)

    # Construct SQL for ATTENDEES table creation with a foreign key constraint
    attendees_cols_str = ", ".join([f"{col_name} {col_type}" for col_name, col_type in ATTENDEES_COLUMNS.items()])
    create_attendees_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {ATTENDEES_TABLE_NAME} (
        {attendees_cols_str},
        FOREIGN KEY (event_id) REFERENCES {EVENTS_TABLE_NAME}(id) ON DELETE CASCADE
    );
    """
    # ON DELETE CASCADE ensures that when an event is deleted, all its associated attendees are also deleted.
    cursor.execute(create_attendees_table_sql)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    # This block allows running `python database.py` to set up the database manually
    create_tables()
    print(f"Database '{DATABASE_NAME}' and tables '{EVENTS_TABLE_NAME}' and '{ATTENDEES_TABLE_NAME}' ensured.")
