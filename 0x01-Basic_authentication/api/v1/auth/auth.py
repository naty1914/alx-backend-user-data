#!/usr/bin/env python3
"""A module for Auth class"""
from flask import request
from typing import List, TypeVar


class Auth():
    """ A class for Authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """A method that determines the authentication is required """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        path = path if path.endswith('/') else path + '/'
        return not any(path.startswith(excluded_path) for
                       excluded_path in excluded_paths)

    def authorization_header(self, request=None) -> str:
        """It checks and returns the authorization header"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ It returns the current user for now none"""
        return None
