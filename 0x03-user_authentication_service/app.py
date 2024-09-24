#!/usr/bin/env python3
"""Flask server"""

from flask import Flask, abort, jsonify, request, redirect

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
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login_user():
    """Creates a new session for the user"""
    email = request.form.get("email")
    pwd = request.form.get("password")
    if AUTH.valid_login(email, pwd):
        session_id = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie("session_id", session_id)
        return resp
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout_user():
    """Resets a user's session, logging them out"""
    sess = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(sess)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    redirect("/")


@app.route("/profile", methods=["GET"])
def get_user():
    """"""
    sess = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(sess)
    if not user:
        abort(403)

    return jsonify({"email": user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
