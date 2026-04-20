from flask import Blueprint, request, jsonify
from backend.models.order_model import create_order

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/create_order', methods=['POST'])
def add_order():
    data = request.json

    customer_id = data.get("customer_id")
    destination = data.get("destination")

    result = create_order(customer_id, destination)

    return jsonify(result)