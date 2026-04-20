from flask import Blueprint, request, jsonify
from backend.models.shipment_model import create_shipment

shipment_bp = Blueprint('shipment_bp', __name__)

@shipment_bp.route('/create_shipment', methods=['POST'])
def add_shipment():
    data = request.json

    order_id = data.get("order_id")
    vehicle_id = data.get("vehicle_id")
    eta = data.get("eta")

    result = create_shipment(order_id, vehicle_id, eta)

    return jsonify(result)