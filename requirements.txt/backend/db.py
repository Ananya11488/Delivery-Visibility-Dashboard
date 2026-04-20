import os
import sqlite3


def get_connection():
    """
    Minimal local DB connection using stdlib sqlite3 so the app runs without extra deps.
    """
    db_path = os.path.join(os.getcwd(), "delivery.db")
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS Orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            order_date TEXT,
            destination TEXT,
            status TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS Shipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT,
            vehicle_id TEXT,
            status TEXT,
            ETA TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS Tracking_Log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shipment_id TEXT,
            timestamp TEXT,
            location TEXT,
            status_update TEXT
        )
        """
    )
    conn.commit()
    return conn
