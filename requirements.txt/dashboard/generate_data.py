import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("delivery.db")
cursor = conn.cursor()

locations = ["Hub A", "Hub B", "Hub C", "City Center"]
statuses = ["In Transit", "Delivered", "Delayed"]

for i in range(100):
    shipment_id = random.randint(1, 10)
    location = random.choice(locations)
    status = random.choice(statuses)
    timestamp = datetime.now() - timedelta(minutes=random.randint(0, 1000))

    cursor.execute("""
    INSERT INTO Tracking_Log (shipment_id, timestamp, location, status_update)
    VALUES (?, ?, ?, ?)
    """, (shipment_id, timestamp, location, status))

conn.commit()
conn.close()

print("✅ Data inserted successfully!")