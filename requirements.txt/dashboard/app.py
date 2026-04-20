import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide")

# -----------------------------
# STYLING (GRADIENT + CARDS)
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #e3f2fd, #fce4ec);
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# DB PATH
# -----------------------------
DB_PATH = r"C:\Users\anany\Downloads\requirements.txt\dashboard\delivery.db"

# -----------------------------
# CONNECTION
# -----------------------------
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# -----------------------------
# LOAD DATA
# -----------------------------
def load_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM Tracking_Log", conn)
    conn.close()
    return df

# -----------------------------
# HEADER
# -----------------------------
st.markdown("## 🚚 Delivery Visibility Dashboard")
st.success("System Status: Live Tracking Enabled ✅")

# -----------------------------
# ADD FORM
# -----------------------------
with st.expander("➕ Add New Tracking Update"):
    with st.form("form"):
        shipment_id = st.text_input("Shipment ID")
        location = st.selectbox("Location", ["Hub A", "Hub B", "Hub C", "City Center"])
        status = st.selectbox("Status", ["In Transit", "Delayed", "Delivered"])

        submitted = st.form_submit_button("Add Update")

        if submitted and shipment_id:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO Tracking_Log (shipment_id, timestamp, location, status_update)
            VALUES (?, ?, ?, ?)
            """, (
                shipment_id,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                location,
                status
            ))

            conn.commit()
            conn.close()

            st.success("✅ Update Added!")
            st.rerun()

# -----------------------------
# LOAD DATA
# -----------------------------
df_full = load_data()
df = df_full.copy()

# -----------------------------
# KPI CARDS
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.markdown(f"""
<div class="card">
<h4>Total Updates</h4>
<h2>{len(df_full)}</h2>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="card">
<h4>Unique Shipments</h4>
<h2>{df_full['shipment_id'].nunique()}</h2>
</div>
""", unsafe_allow_html=True)

delayed_count = (df_full['status_update'] == "Delayed").sum()

col3.markdown(f"""
<div class="card">
<h4>Delayed Shipments</h4>
<h2>{delayed_count}</h2>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# FILTER
# -----------------------------
status_filter = st.selectbox(
    "Filter by Status",
    ["All", "In Transit", "Delayed", "Delivered"],
    key="status_filter"
)

# Apply filter ONLY to df (not df_full)
if status_filter != "All":
    df = df_full[df_full["status_update"] == status_filter]
else:
    df = df_full.copy()

# -----------------------------
# TABLE
# -----------------------------
st.markdown("## 📋 Tracking Data")

st.dataframe(df, use_container_width=True, height=400)
st.markdown("### 🗑️ Delete a Tracking Update")

if not df.empty:
    selected_id = st.selectbox(
        "Select ID to delete",
        df["id"].tolist()
    )

    if st.button("Delete Selected Row"):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Tracking_Log WHERE id = ?", (selected_id,))

        conn.commit()
        conn.close()

        st.success(f"Deleted row with ID {selected_id}")
        st.rerun()

# -----------------------------
# STATUS CHARTS SIDE BY SIDE
# -----------------------------
st.markdown("## 📊 Status Distribution")

colA, colB = st.columns(2)

status_counts = df["status_update"].value_counts()

with colA:
    fig1, ax1 = plt.subplots()
    ax1.bar(status_counts.index, status_counts.values)
    ax1.set_title("Status Count")
    st.pyplot(fig1)

with colB:
    fig2, ax2 = plt.subplots()
    ax2.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%")
    ax2.set_title("Status %")
    st.pyplot(fig2)


# TIME SERIES + LOCATION SIDE BY SIDE
# -----------------------------
st.markdown("## 📈 Insights")

colC, colD = st.columns(2)

# ✅ TIME SERIES 
with colC:
    st.markdown("### Tracking Over Time")

    df_time = df.copy()
    df_time["timestamp"] = pd.to_datetime(df_time["timestamp"], errors="coerce")
    df_time = df_time.dropna(subset=["timestamp"])

    df_time = df_time.sort_values("timestamp")

    if not df_time.empty:
        df_time["count"] = range(1, len(df_time) + 1)
        st.line_chart(df_time.set_index("timestamp")["count"])
    else:
        st.warning("No valid timestamp data")


# LOCATION
with colD:
    location_counts = df["location"].value_counts()

    fig4, ax4 = plt.subplots()
    ax4.bar(location_counts.index, location_counts.values)
    ax4.set_title("Location Distribution")
    st.pyplot(fig4)

# -----------------------------
# DELAY SECTION
# -----------------------------
st.markdown("## ⏱️ Delay Prediction")

# -----------------------------
# PREP DATA
# -----------------------------
df_full["timestamp"] = pd.to_datetime(df_full["timestamp"], errors="coerce")

# STEP 1: Create ETA FIRST
df_full["ETA"] = df_full["timestamp"] + pd.to_timedelta(30, unit="m")

# STEP 2: Then calculate delay
current_time = pd.Timestamp.now()

df_full["delay_status"] = df_full.apply(
    lambda row: "Delayed"
    if row["status_update"] != "Delivered" and current_time > row["ETA"]
    else "On Time",
    axis=1
)

st.dataframe(df_full[["shipment_id", "timestamp", "ETA", "delay_status"]])

delay_counts = df_full["delay_status"].value_counts()

fig5, ax5 = plt.subplots()
ax5.bar(delay_counts.index, delay_counts.values)
ax5.set_title("Delay Prediction")
st.pyplot(fig5)

# -----------------------------
# INSIGHTS
# -----------------------------
st.markdown("## 📌 Key Insights")

st.write(f"• {round((delayed_count / len(df_full)) * 100, 1)}% of shipments are delayed.")
st.write(f"• Most frequent status: {df_full['status_update'].mode()[0]}")
st.write(f"• Most active location: {df_full['location'].mode()[0]}")