#!/usr/bin/env python3
"""
    Basic Authenication Module
"""
from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar


class BasicAuth(Auth):
    """
        Basic Authentication Class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
            returns the Base64 part of the Authorization
            header for Basic Authentication
        """
        if not authorization_header or type(authorization_header) != str:
            return None

        if not authorization_header.startswith('Basic'):
            return None

        if len(authorization_header) > 5:
            if authorization_header[5:6] == ' ':
                return authorization_header[6:]
        return None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
            returns the decoded string from the base64 string
            gotten from the authorization header
        """
        if not base64_authorization_header:
            return None

        if type(base64_authorization_header) != str:
            return None

        try:
            # decode the string if it's in base64
            b64_decode = base64.b64decode(base64_authorization_header)
            return b64_decode.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str
                                 ) -> Tuple[str, str]:
        """
            returns the user email and password from the base64 decoded value
        """
        if not decoded_base64_authorization_header:
            return (None, None)

        if type(decoded_base64_authorization_header) != str:
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        user_pass = decoded_base64_authorization_header.split(':')
        return tuple(user_pass)

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """
            returns the user instance based on his email and password
        """
        if user_email is None or type(user_email) != str:
            return None

        if user_pwd is None or type(user_pwd) != str:
            return None
