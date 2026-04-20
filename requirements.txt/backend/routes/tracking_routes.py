from flask import Blueprint, request, jsonify
from backend.models.tracking_model import add_tracking, get_tracking_data

tracking_bp = Blueprint("tracking_bp", __name__)


@tracking_bp.route("/add_tracking", methods=["POST"])
def tracking():
    data = request.json or {}

    shipment_id = data.get("shipment_id")
    location = data.get("location")
    status = data.get("status")

    result = add_tracking(shipment_id, location, status)
    return jsonify(result)


@tracking_bp.route("/get_tracking", methods=["GET"])
def get_tracking():
    data = get_tracking_data()
    return jsonify(data)