#!/usr/bin/env python3
"""
    App module
"""
from flask import Flask, jsonify, request, abort, redirect
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
    email, passwd = request.form.get('email'), request.form.get('password')

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
    if request.method == 'POST':
        email, passwd = request.form.get('email'), request.form.get('password')

        if not auth.valid_login(email, passwd):
            abort(401)

        ses_id = auth.create_session(email)
        payload = jsonify({"email": email, "message": "logged in"})
        payload.set_cookie('session_id', ses_id)
        return payload
    else:
        ses_id = request.cookies.get('session_id')
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
    ses_id = request.cookies.get('session_id')
    user_inst = auth.get_user_from_session_id(ses_id)
    if user_inst:
        return jsonify({"email": user_inst.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
        gets the reset password token, from the email provided
        in the form
    """
    email = request.form.get('email')
    try:
        reset_tok = auth.get_reset_passowrd_token(email)
    except ValueError:
        abort(403)
    return jsonify({
        "email": email,
        "reset_token": reset_tok
    }), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """
        updates the user password based on email, reset_token
        and new_password from the form
    """
    email, res_tok = request.form.get('email'), request.form.get('reset_token')
    new_passwd = request.form.get('new_password')

    try:
        auth.update_password(res_tok, new_passwd)
    except ValueError:
        abort(403)

    # check if email and password can be used to login
    if auth.valid_login(email, new_passwd):
        abort(403)

    return jsonify({
        "email": f"{email}",
        "message": "Password updated"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
