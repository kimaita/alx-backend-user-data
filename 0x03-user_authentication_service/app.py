#!/usr/bin/env python3
"""Flask server"""

from flask import jsonify, Flask, request
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/")
def welcome():
    """Returns a welcome message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """Endpoint for registering a new user"""
    try:
        email = request.form.get("email")
        pwd = request.form.get("password")
        user = AUTH.register_user(email, pwd)
        if user:
            return jsonify({"email": email, "message": "user created"})
    except KeyError:
        return
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
