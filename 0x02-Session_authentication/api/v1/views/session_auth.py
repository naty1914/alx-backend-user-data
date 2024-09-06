#!/usr/bin/env python3
"""A module that  handles all routes for the Session authentication"""

import os
from flask import request, jsonify, abort
from typing import Tuple
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """It handles the POST /auth_session/login route"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404

    if users[0].is_valid_password(password):
        from api.v1.app import auth
        sessiond_id = auth.create_session(getattr(users[0], 'id'))
        resp = jsonify(users[0].to_json())
        resp.set_cookie(os.getenv('SESSION_NAME'), sessiond_id)
        return resp

    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> Tuple[str, int]:
    """It handles the DELETE /auth_session/logout route"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({})
