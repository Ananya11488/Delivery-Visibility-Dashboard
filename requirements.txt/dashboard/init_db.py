import sqlite3

conn = sqlite3.connect("delivery.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS Tracking_Log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shipment_id TEXT,
    timestamp TEXT,
    location TEXT,
    status_update TEXT
)
""")

conn.commit()
conn.close()

print("✅ Tables created successfully!")