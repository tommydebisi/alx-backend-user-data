#!/usr/bin/env python3
"""
    Module of Session Authentication view
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_user() -> str:
    """ authenticating user on site """
    from api.v1.app import auth

    email, password = request.form.get('email'), request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    user_inst = User.search({'email': email})
    if not user_inst:
        return jsonify({"error": "no user found for this email"}), 404

    if not user_inst[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    ses_id = auth.create_session(user_inst[0].id)
    cookie_name = getenv('SESSION_NAME')

    out = jsonify(user_inst[0].to_json())
    out.set_cookie(cookie_name, ses_id)
    return out


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout_user():
    """ log out the user """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
