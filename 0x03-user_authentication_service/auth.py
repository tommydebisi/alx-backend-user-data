#!/usr/bin/env python3
"""
    auth module
"""
from db import DB, User
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """
        returns salted hash of the input password
    """
    encoded_pass = password.encode('utf-8')
    return hashpw(encoded_pass, gensalt())


def _generate_uuid() -> str:
    """
        generates a new unique string id
    """
    return str(uuid4())


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

    def create_session(self, email: str) -> str:
        """
            gets a user affiliated with email, stores the unique
            session id to the database and return it
        """
        try:
            usr_inst = self._db.find_user_by(email=email)
        except (InvalidRequestError, NoResultFound):
            return None

        ses_id = _generate_uuid()
        self._db.update_user(usr_inst.id, session_id=ses_id)
        return ses_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
            returns the User instance from the given session id or None
            if not found
        """
        try:
            usr_inst = self._db.find_user_by(session_id=session_id)
        except (InvalidRequestError, NoResultFound):
            return None
        return usr_inst

    def destroy_session(self, user_id: str) -> None:
        """
            destroys session relating to the user_id provided
            or does nothing if user_id is not present in the database
        """
        self._db.update_user(user_id, session_id=None)
