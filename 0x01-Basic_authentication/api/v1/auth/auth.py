#!/usr/bin/env python3
"""A module for Auth class"""
import re
from flask import request
from typing import List, TypeVar


class Auth():
    """ A class for Authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """It checks if the path is excluded"""
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

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
