# config.py

DATABASE_NAME = "myevent.db"

# Event Table Configuration
EVENTS_TABLE_NAME = "events"
EVENTS_COLUMNS = {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "name": "TEXT NOT NULL",
    "date": "TEXT NOT NULL", # Stored as YYYY-MM-DD
    "description": "TEXT"
}

# Attendee Table Configuration
ATTENDEES_TABLE_NAME = "attendees"
ATTENDEES_COLUMNS = {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "event_id": "INTEGER NOT NULL", # Foreign key linking to events table
    "name": "TEXT NOT NULL",
    "email": "TEXT NOT NULL"
}
