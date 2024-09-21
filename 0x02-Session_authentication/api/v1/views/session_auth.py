#!/usr/bin/env python3
"""Handles Flask route authentication"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route("/auth_session/login", methods=["POST"])
def authenticate_user():
    """POST /auth_session/login

    Return:
        the user object with a session_id cookie
    """
    email = request.form.get("email")
    pwd = request.form.get("password")
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not pwd:
        return jsonify({"error": "password missing"}), 400
    try:
        user = User.search({"email": email})[0]
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not user.is_valid_password(pwd):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    user_resp = jsonify(user.to_json())
    sess_cookie = os.getenv("SESSION_NAME")
    if sess_cookie:
        user_resp.set_cookie(sess_cookie, session_id)

    return user_resp
