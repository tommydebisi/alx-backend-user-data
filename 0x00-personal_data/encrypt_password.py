#!/usr/bin/env python3
""" encrypt_password mod """
import bcrypt


def hash_password(password: str) -> bytes:
    """
        takes in a password and returns a salted, hased pasword
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
        checks if the given hashed password and password
        are the same and return true if same or false if not
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
