from backend.db import get_connection

def add_tracking(shipment_id, location, status):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO Tracking_Log (shipment_id, timestamp, location, status_update)
    VALUES (?, datetime('now'), ?, ?)
    """

    cursor.execute(query, (shipment_id, location, status))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Tracking updated"}


def get_tracking_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT shipment_id, timestamp, location, status_update
        FROM Tracking_Log
        ORDER BY id DESC
        """
    )
    rows = cursor.fetchall()
    cols = [d[0] for d in cursor.description] if cursor.description else []

    cursor.close()
    conn.close()

    return [dict(zip(cols, row)) for row in rows]