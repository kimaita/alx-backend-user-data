#!/usr/bin/env python3
"""
Route module for the API
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS


def not_found(error) -> str:
    """Not found handler"""
    return jsonify({"error": "Not found"}), 404


def unauthorized(error) -> str:
    """Unauthorised request error handler"""
    return jsonify({"error": "Unauthorized"}), 401


def forbidden_res(error) -> str:
    """Forbidden resource error handler"""
    return jsonify({"error": "Forbidden"}), 403


app = Flask(__name__)
app.register_blueprint(app_views)
app.register_error_handler(401, unauthorized)
app.register_error_handler(403, forbidden_res)
app.register_error_handler(404, not_found)

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)