from backend.db import get_connection

def create_order(customer_id, destination):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO Orders (customer_id, order_date, destination, status)
    VALUES (?, datetime('now'), ?, ?)
    """

    cursor.execute(query, (customer_id, destination, "Pending"))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Order created successfully"}