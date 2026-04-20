from flask import Flask
from backend.routes.order_routes import order_bp
from backend.routes.shipment_routes import shipment_bp
from backend.routes.tracking_routes import tracking_bp

app = Flask(__name__)

# Register routes
app.register_blueprint(order_bp)
app.register_blueprint(shipment_bp)
app.register_blueprint(tracking_bp)

#region agent log
import json, os, time  # noqa: E401
def _agent_log(message, data=None, hypothesisId="R1", runId="pre-fix"):
    try:
        _project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        _log_path = os.path.join(_project_root, "debug-779f0e.log")
        payload = {
            "sessionId": "779f0e",
            "runId": runId,
            "hypothesisId": hypothesisId,
            "location": "backend/app.py:routes_log",
            "message": message,
            "data": data or {},
            "timestamp": int(time.time() * 1000),
        }
        with open(_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
    except Exception:
        pass

_agent_log("Flask routes at startup", data={"rules": [str(r) for r in app.url_map.iter_rules()]}, hypothesisId="R1", runId="pre-fix")
#endregion


@app.route("/")
def home():
    return "Delivery Visibility System Running"

if __name__ == "__main__":
    app.run(debug=True)