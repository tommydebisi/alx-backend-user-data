#!/usr/bin/env python3
"""
    auth module
"""
from db import DB, User
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
        returns salted hash of the input password
    """
    encoded_pass = password.encode('utf-8')
    return hashpw(encoded_pass, gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
            takes user's email and password and returns the
            user instance associated with it
        """
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
        except (InvalidRequestError, NoResultFound):
            hashed_pass = _hash_password(password)
            return self._db.add_user(email, hashed_pass.decode('utf-8'))

    def valid_login(self, email: str, password: str) -> bool:
        """
            Checks login details and returns True if info provided
            is correct else it returns False
        """
        try:
            usr_inst = self._db.find_user_by(email=email)
            return checkpw(password.encode('utf-8'),
                           usr_inst.hashed_password.encode('utf-8'))
        except (InvalidRequestError, NoResultFound):
            return False
