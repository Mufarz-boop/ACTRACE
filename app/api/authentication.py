import hmac
from functools import wraps
from flask import current_app, request, jsonify

def shared_key_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        expected = current_app.config.get("SHARED_API_KEY", "")
        received = request.headers.get("X-API-Key", "")
        if not expected:
            return jsonify({"success": False, "message": "API belum dikonfigurasi."}), 503
        if not received or not hmac.compare_digest(received, expected):
            return jsonify({"success": False, "message": "API key tidak valid."}), 401
        return view(*args, **kwargs)
    return wrapped