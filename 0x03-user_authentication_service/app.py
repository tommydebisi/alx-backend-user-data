#!/usr/bin/env python3
"""
    App module
"""
from flask import Flask, jsonify, request as rq, abort, redirect
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


@app.route('/sessions', methods=['POST', 'DELETE'], strict_slashes=False)
def login():
    """
        Login users
    """
    if rq.method == 'POST':
        email, passwd = rq.form.get('email'), rq.form.get('password')

        if not auth.valid_login(email, passwd):
            abort(401)

        ses_id = auth.create_session(email)
        payload = jsonify({"email": email, "message": "logged in"})
        payload.set_cookie('session_id', ses_id)
        return payload
    else:
        ses_id = rq.cookies.get('session_id')
        usr_inst = auth.get_user_from_session_id(ses_id)

        if usr_inst is None:
            abort(403)

        auth.destroy_session(usr_inst.id)
        return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
        Display user profile payload
    """
    ses_id = rq.cookies.get('session_id')
    user_inst = auth.get_user_from_session_id(ses_id)
    if user_inst:
        return jsonify({"email": user_inst.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
