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
        if not path or not excluded_paths:
            return True

        for strr in excluded_paths:
            if strr.endswith('*'):
                spl_ex = strr.split('/')[-1]

                # check for ending with '/' and not ending with '/'
                spl_path = path.split('/')[-1] if not path.endswith('/') \
                    else path.split('/')[-2]

                if spl_path.startswith(spl_ex[:-1]):
                    return False

            if strr.endswith('/'):
                if path in strr[:-1] or path[:-1] in strr[:-1]:
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
