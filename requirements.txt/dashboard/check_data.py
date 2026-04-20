import sqlite3

conn = sqlite3.connect("delivery.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM Tracking_Log")
print("Total rows:", cursor.fetchone()[0])

conn.close()