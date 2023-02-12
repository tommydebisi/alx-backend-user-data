#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = os.getenv('AUTH_TYPE', None)

if auth:
    from api.v1.auth.auth import Auth
    from api.v1.auth.basic_auth import BasicAuth
    from api.v1.auth.session_auth import SessionAuth
    from api.v1.auth.session_exp_auth import SessionExpAuth
    from api.v1.auth.session_db_auth import SessionDBAuth

    if auth == 'basic_auth':
        auth = BasicAuth()
    elif auth == 'session_auth':
        auth = SessionAuth()
    elif auth == 'session_exp_auth':
        auth = SessionExpAuth()
    elif auth == 'session_db_auth':
        auth = SessionDBAuth()
    else:
        auth = Auth()


@app.before_request
def before_req() -> None:
    """
        checks authorization header and validates the
        current user
    """
    if not auth:
        return

    ex_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                '/api/v1/forbidden/', '/api/v1/auth_session/login/',
                '/api/v1/auth_session/logout/']

    # check if path is part of the excluded paths and do nothing
    if not auth.require_auth(request.path, ex_paths):
        return

    authoriz = auth.authorization_header(request)
    if not authoriz and not auth.session_cookie(request):
        abort(401)  # user needs to be authenticated

    request.current_user = auth.current_user(request)
    if request.current_user is None:
        abort(403)  # user has no right to the content


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def req_unauthorized(error) -> str:
    """
        unauthorized request handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
        forbidden request from user
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
