#!/usr/bin/env python3
"""
    App module
"""
from flask import Flask, jsonify, request as rq
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def basic():
    """
        basic function to return a payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def reg_user():
    """
        Registers users
    """
    email, passwd = rq.form.get('email'), rq.form.get('password')

    try:
        auth.register_user(email, passwd)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
