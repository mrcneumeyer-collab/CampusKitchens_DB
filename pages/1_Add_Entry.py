import streamlit as st
import psycopg2

st.set_page_config(page_title="Add Food Entry", page_icon="➕")

def get_connection():
    return psycopg2.connect(st.secrets["DB_URL1"])

st.title("➕ Add a New Food Entry")

with st.form("add_entry_form"):
    entry_date = st.text_input("Date", placeholder="Example: 1/22/2024 or 2024-01-22")
    location = st.text_input("Location", placeholder="Example: GFH")
    item = st.text_input("Item", placeholder="Example: Beans")
    quantity = st.text_input("Quantity", placeholder="Example: 25")

    submitted = st.form_submit_button("Add Entry")

    if submitted:
        if entry_date and location and item and quantity:
            try:
                conn = get_connection()
                cur = conn.cursor()

                cur.execute("""
                    INSERT INTO food_entries_master (date, location, item, quantity)
                    VALUES (%s, %s, %s, %s);
                """, (entry_date, location, item, quantity))

                conn.commit()
                cur.close()
                conn.close()

                st.success(f"✅ Entry added successfully: {item} at {location}")
            except Exception as e:
                st.error(f"Error adding entry: {e}")
        else:
            st.warning("Please fill in all fields.")
