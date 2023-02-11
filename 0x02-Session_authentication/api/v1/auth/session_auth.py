#!/usr/bin/env python3
"""
    Session Based Authentication
"""
from api.v1.auth.auth import Auth, request
from models.user import User
from uuid import uuid4
from typing import TypeVar


class SessionAuth(Auth):
    """
        Session Authentication class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
            returns the session id for the user
            provided
        """
        if user_id is None or type(user_id) != str:
            return None

        ses_id = str(uuid4())
        self.user_id_by_session_id[ses_id] = user_id
        return ses_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
            returns a user id based on the given session id
        """
        if session_id is None or type(session_id) != str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """
            returns the user instance based on session auth
        """
        ses_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(ses_cookie)

        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """
            destroys a user's current session
        """
        if request is None:
            return False

        ses_id = self.session_cookie(request)
        if not ses_id:
            return False

        if not self.user_id_for_session_id(ses_id):
            return False

        del self.user_id_for_session_id[ses_id]
        return True
