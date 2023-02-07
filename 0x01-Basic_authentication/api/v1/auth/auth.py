#!/usr/bin/env python3
"""
    Module coovering authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
        Authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            returns True if path is part of the excluded paths or false if
            not
        """
        if not path:
            return True

        if path in excluded_paths or path[:-1] in excluded_paths:
            return False

        for strr in excluded_paths:
            if strr.endswith('*'):
                spl_ex = strr.split('/')[-1]
                spl_path = path.split('/')[-1]

                if spl_path.startswith(spl_ex[:-1]):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
            returns none for now

            Args:
                request: flask request object
        """
        if request is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
            returns none for now

            Args:
                request: flask request object
        """
        return None
