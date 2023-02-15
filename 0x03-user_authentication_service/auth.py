#!/usr/bin/env python3
"""
    auth module
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """
        returns salted hash of the input password
    """
    encoded_pass = password.encode('utf-8')
    return hashpw(encoded_pass, gensalt())
