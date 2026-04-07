import streamlit as st
import psycopg2

st.set_page_config(page_title="Food Entry Database App", page_icon="🍽️")

def get_connection():
    return psycopg2.connect(st.secrets["DB_URL"])

st.title("🍽️ Food Entry Database App")
st.write("Welcome! Use the sidebar to navigate between pages.")

st.markdown("---")
st.subheader("📊 Current Data")

try:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM food_entries_master;")
    entry_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT location) FROM food_entries_master;")
    location_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT item) FROM food_entries_master;")
    item_count = cur.fetchone()[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Entries", entry_count)
    col2.metric("Locations", location_count)
    col3.metric("Items", item_count)

    st.markdown("---")
    st.subheader("📋 All Food Entries")

    cur.execute("""
        SELECT id, date, location, item, quantity
        FROM food_entries_master
        ORDER BY id ASC;
    """)
    rows = cur.fetchall()

    if rows:
        st.dataframe(
            [
                {
                    "ID": r[0],
                    "Date": r[1],
                    "Location": r[2],
                    "Item": r[3],
                    "Quantity": r[4]
                }
                for r in rows
            ],
            use_container_width=True
        )
    else:
        st.info("No food entries found yet.")

    cur.close()
    conn.close()

except Exception as e:
    st.error(f"Database connection error: {e}")