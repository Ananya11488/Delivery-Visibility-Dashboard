from backend.db import get_connection

def create_shipment(order_id, vehicle_id, eta):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO Shipment (order_id, vehicle_id, status, ETA)
    VALUES (?, ?, ?, ?)
    """

    cursor.execute(query, (order_id, vehicle_id, "In Transit", eta))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Shipment created successfully"}