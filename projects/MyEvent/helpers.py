# helpers.py
import sqlite3
from database import get_db_connection
from config import EVENTS_TABLE_NAME, ATTENDEES_TABLE_NAME

# --- Event Functions ---

def create_event(name, date, description):
    """Adds a new event to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"INSERT INTO {EVENTS_TABLE_NAME} (name, date, description) VALUES (?, ?, ?)",
            (name, date, description)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error creating event: {e}")
        return False
    finally:
        conn.close()

def get_all_events():
    """Retrieves all events from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {EVENTS_TABLE_NAME} ORDER BY date DESC, name ASC")
    events = cursor.fetchall()
    conn.close()
    # Convert Row objects to dictionaries for easier handling in Streamlit
    return [dict(event) for event in events]

def get_event_by_id(event_id):
    """Retrieves a single event by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {EVENTS_TABLE_NAME} WHERE id = ?", (event_id,))
    event = cursor.fetchone()
    conn.close()
    return dict(event) if event else None

def update_event(event_id, name, date, description):
    """Updates an existing event in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"UPDATE {EVENTS_TABLE_NAME} SET name = ?, date = ?, description = ? WHERE id = ?",
            (name, date, description, event_id)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating event: {e}")
        return False
    finally:
        conn.close()

def delete_event(event_id):
    """Deletes an event from the database. This will also delete associated attendees due to ON DELETE CASCADE."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM {EVENTS_TABLE_NAME} WHERE id = ?", (event_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting event: {e}")
        return False
    finally:
        conn.close()

# --- Attendee Functions ---

def add_attendee_to_event(event_id, name, email):
    """Adds a new attendee to a specific event."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"INSERT INTO {ATTENDEES_TABLE_NAME} (event_id, name, email) VALUES (?, ?, ?)",
            (event_id, name, email)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error adding attendee: {e}")
        return False
    finally:
        conn.close()

def get_attendees_for_event(event_id):
    """Retrieves all attendees for a specific event."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {ATTENDEES_TABLE_NAME} WHERE event_id = ? ORDER BY name ASC", (event_id,))
    attendees = cursor.fetchall()
    conn.close()
    return [dict(attendee) for attendee in attendees]

def delete_attendee(attendee_id):
    """Deletes an attendee from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM {ATTENDEES_TABLE_NAME} WHERE id = ?", (attendee_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting attendee: {e}")
        return False
    finally:
        conn.close()
