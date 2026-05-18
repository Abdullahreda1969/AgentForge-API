import streamlit as st
import pandas as pd
from datetime import datetime
import helpers
import database # To ensure tables are created on startup

# Initialize database tables if they don't exist
database.create_tables()

# --- Session State Initialization ---
# Using st.session_state to manage application state across reruns
if 'page' not in st.session_state:
    st.session_state.page = 'view_events' # Default page
if 'selected_event_id' not in st.session_state:
    st.session_state.selected_event_id = None # Store ID of the currently selected event
if 'editing_event' not in st.session_state:
    st.session_state.editing_event = None # Store event data when in edit mode

# --- Callback for st.dataframe selection ---
def handle_event_selection(event):
    """Callback function to update selected_event_id based on dataframe selection."""
    if event.selection.rows:
        # `event.selection.rows` contains the 0-based index of the selected row in the displayed DataFrame.
        selected_index = event.selection.rows[0]
        # We need the original event object to get its `id`
        all_events_data = helpers.get_all_events() # Re-fetch to ensure fresh data and proper indexing
        if selected_index < len(all_events_data):
            st.session_state.selected_event_id = all_events_data[selected_index]['id']
        else:
            st.session_state.selected_event_id = None # Should not happen if data is consistent
    else:
        st.session_state.selected_event_id = None # No row selected

# --- UI Functions for Pages ---

def show_view_events_page():
    """Displays all events in a selectable table and allows actions."""
    st.title("🗓️ MyEvent - Event Management")
    st.subheader("All Events")

    events = helpers.get_all_events()

    if not events:
        st.info("No events found. Add a new event using the 'Add New Event' button in the sidebar.")
        # Provide an in-page button as well for convenience
        if st.button("Add New Event", key="add_new_event_empty_state"):
            st.session_state.page = 'add_event'
            st.rerun()
        return

    df = pd.DataFrame(events)
    df_display = df.copy()
    # Format date for better display in the UI
    df_display['date'] = pd.to_datetime(df_display['date']).dt.strftime('%Y-%m-%d')

    st.markdown("Select an event from the table below to view/manage attendees or edit/delete.")

    # Use st.dataframe with `on_select` callback as per critical rule.
    st.dataframe(
        df_display[['name', 'date', 'description']], # Display relevant columns
        on_select=handle_event_selection, # Callback for row selection
        selection_mode="single-row",      # Allow single row selection
        use_container_width=True,         # Make dataframe responsive
        hide_index=True,                  # Don't show pandas index
        key="events_dataframe"            # Unique key for the dataframe
    )

    if st.session_state.selected_event_id:
        selected_event_data = helpers.get_event_by_id(st.session_state.selected_event_id)
        if selected_event_data:
            st.subheader(f"Actions for Event: {selected_event_data['name']}")

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Manage Attendees", key=f"manage_attendees_{selected_event_data['id']}"):
                    st.session_state.page = 'manage_attendees'
                    st.rerun()
            with col2:
                if st.button("Edit Event", key=f"edit_event_{selected_event_data['id']}"):
                    st.session_state.editing_event = selected_event_data
                    st.session_state.page = 'edit_event'
                    st.rerun()
            with col3:
                # Confirm deletion with a warning
                if st.button("Delete Event", key=f"delete_event_{selected_event_data['id']}", type="secondary"):
                    st.warning(f"Are you sure you want to delete '{selected_event_data['name']}'? This action cannot be undone and will also delete all associated attendees.")
                    if st.button("Confirm Delete", key=f"confirm_delete_{selected_event_data['id']}"):
                        if helpers.delete_event(selected_event_data['id']):
                            st.success(f"Event '{selected_event_data['name']}' and its attendees deleted successfully.")
                            st.session_state.selected_event_id = None # Clear selection
                            st.rerun() # Refresh UI
                        else:
                            st.error("Error deleting event.")
        else:
            # Handle case where selected event might have been deleted by another action
            st.session_state.selected_event_id = None
            st.warning("Selected event not found. Please re-select or refresh.")
            st.rerun() # Force a rerun to clear stale state
    else:
        st.info("Select an event from the table above to perform actions.")

def show_add_event_page():
    """Displays a form to add a new event."""
    st.title("➕ Add New Event")

    with st.form("add_event_form", clear_on_submit=True):
        st.write("Enter event details:")
        name = st.text_input("Event Name", help="e.g., Annual Tech Conference")
        date_obj = st.date_input("Event Date", datetime.now().date(), help="Date of the event")
        description = st.text_area("Description", help="Brief description of the event (optional)")

        submitted = st.form_submit_button("Add Event") # CRITICAL: use st.form_submit_button
        if submitted:
            if name and date_obj:
                date_str = date_obj.strftime("%Y-%m-%d")
                if helpers.create_event(name, date_str, description):
                    st.success(f"Event '{name}' added successfully!")
                    st.session_state.page = 'view_events' # Navigate back to view events
                    st.rerun() # CRITICAL: rerun after data modification
                else:
                    st.error("Failed to add event. Please try again.")
            else:
                st.warning("Please fill in Event Name and Date.")

def show_edit_event_page():
    """Displays a form to edit an existing event."""
    if not st.session_state.editing_event:
        st.warning("No event selected for editing. Please select an event from 'View Events'.")
        st.session_state.page = 'view_events'
        st.rerun()
        return

    event = st.session_state.editing_event
    st.title(f"✍️ Edit Event: {event['name']}")

    with st.form("edit_event_form"):
        st.write(f"Editing details for Event ID: {event['id']}")
        name = st.text_input("Event Name", value=event['name'], help="e.g., Annual Tech Conference")
        # Convert stored date string back to datetime.date object for st.date_input
        date_obj = st.date_input("Event Date", value=datetime.strptime(event['date'], "%Y-%m-%d").date(), help="Date of the event")
        description = st.text_area("Description", value=event['description'], help="Brief description of the event (optional)")

        submitted = st.form_submit_button("Update Event") # CRITICAL: use st.form_submit_button
        if submitted:
            if name and date_obj:
                date_str = date_obj.strftime("%Y-%m-%d")
                if helpers.update_event(event['id'], name, date_str, description):
                    st.success(f"Event '{name}' updated successfully!")
                    st.session_state.editing_event = None # Clear editing state
                    st.session_state.page = 'view_events' # Go back to event list
                    st.rerun() # CRITICAL: rerun after data modification
                else:
                    st.error("Failed to update event. Please try again.")
            else:
                st.warning("Please fill in Event Name and Date.")
    
    # Button to cancel editing and go back
    if st.button("⬅ Cancel Edit", key="cancel_edit_event"):
        st.session_state.editing_event = None
        st.session_state.page = 'view_events'
        st.rerun()

def show_manage_attendees_page():
    """Displays and manages attendees for a selected event."""
    if not st.session_state.selected_event_id:
        st.warning("No event selected. Please select an event from 'View Events'.")
        st.session_state.page = 'view_events'
        st.rerun()
        return

    event_id = st.session_state.selected_event_id
    event = helpers.get_event_by_id(event_id)

    if not event:
        st.error("Selected event not found. Returning to 'View Events'.")
        st.session_state.selected_event_id = None # Clear invalid selection
        st.session_state.page = 'view_events'
        st.rerun()
        return

    st.title(f"👥 Manage Attendees for: {event['name']}")
    st.markdown(f"**Date:** {event['date']} | **Description:** {event['description']}")

    st.subheader("Add New Attendee")
    with st.form("add_attendee_form", clear_on_submit=True):
        attendee_name = st.text_input("Attendee Name", help="e.g., John Doe")
        attendee_email = st.text_input("Attendee Email", help="e.g., john.doe@example.com")
        
        add_attendee_submitted = st.form_submit_button("Add Attendee") # CRITICAL: use st.form_submit_button
        if add_attendee_submitted:
            if attendee_name and attendee_email:
                if helpers.add_attendee_to_event(event_id, attendee_name, attendee_email):
                    st.success(f"Attendee '{attendee_name}' added to {event['name']}!")
                    st.rerun() # CRITICAL: rerun after data modification
                else:
                    st.error("Failed to add attendee.")
            else:
                st.warning("Please fill in Attendee Name and Email.")

    st.subheader("Current Attendees")
    attendees = helpers.get_attendees_for_event(event_id)

    if not attendees:
        st.info(f"No attendees registered for {event['name']} yet.")
    else:
        # Display attendees in a structured way with a delete button for each
        # Using columns for better alignment and individual delete buttons
        st.markdown("| # | Name | Email | |")
        st.markdown("|:---|:---|:---|:---|")
        for idx, attendee in enumerate(attendees):
            col1, col2, col3, col4 = st.columns([0.5, 2, 2.5, 1])
            with col1:
                st.write(f"**{idx+1}.**")
            with col2:
                st.write(attendee['name'])
            with col3:
                st.write(attendee['email'])
            with col4:
                if st.button("Delete", key=f"delete_attendee_{attendee['id']}", type="secondary"):
                    st.warning(f"Are you sure you want to delete attendee '{attendee['name']}'?")
                    if st.button("Confirm", key=f"confirm_delete_attendee_{attendee['id']}"):
                        if helpers.delete_attendee(attendee['id']):
                            st.success(f"Attendee '{attendee['name']}' removed.")
                            st.rerun() # CRITICAL: rerun after data modification
                        else:
                            st.error("Error deleting attendee.")

    st.markdown("---<br>", unsafe_allow_html=True)
    if st.button("⬅ Back to Events", key="back_to_events_from_attendees"):
        st.session_state.selected_event_id = None # Clear selection
        st.session_state.page = 'view_events'
        st.rerun()


# --- Sidebar Navigation ---
st.sidebar.title("Navigation")

# Main navigation buttons
if st.sidebar.button("View Events", key="nav_view_events"):
    st.session_state.page = 'view_events'
    st.session_state.selected_event_id = None # Clear selection when changing page
    st.session_state.editing_event = None
    st.rerun()
if st.sidebar.button("Add New Event", key="nav_add_event"):
    st.session_state.page = 'add_event'
    st.session_state.selected_event_id = None
    st.session_state.editing_event = None
    st.rerun()

# Dynamic sidebar actions for a selected event
# These buttons only appear if an event is selected AND we're not already on a specific action page for it
if st.session_state.selected_event_id and st.session_state.page not in ['manage_attendees', 'edit_event']:
    selected_event_name = helpers.get_event_by_id(st.session_state.selected_event_id)
    if selected_event_name:
        st.sidebar.markdown("---<br>", unsafe_allow_html=True)
        st.sidebar.subheader("Selected Event Actions")
        st.sidebar.markdown(f"*Currently selected:* **{selected_event_name['name']}**")

        if st.sidebar.button(f"Manage Attendees for '{selected_event_name['name']}'", key="sidebar_manage_attendees"):
            st.session_state.page = 'manage_attendees'
            st.session_state.editing_event = None
            st.rerun()
        if st.sidebar.button(f"Edit '{selected_event_name['name']}'", key="sidebar_edit_event"):
            st.session_state.editing_event = selected_event_name # Set event data for editing
            st.session_state.page = 'edit_event'
            st.rerun()

# --- Main Content Renderer ---
# Based on the current page in session_state, render the appropriate UI function
if st.session_state.page == 'view_events':
    show_view_events_page()
elif st.session_state.page == 'add_event':
    show_add_event_page()
elif st.session_state.page == 'manage_attendees':
    show_manage_attendees_page()
elif st.session_state.page == 'edit_event':
    show_edit_event_page()
