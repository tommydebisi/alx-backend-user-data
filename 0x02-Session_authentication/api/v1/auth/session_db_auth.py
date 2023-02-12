#!/usr/bin/env python3
"""
    session database auth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
        session db class
    """
    def create_session(self, user_id: str = None) -> str:
        """
            creates and returns a new session id with expiration date
        """
        ses_id = super().create_session(user_id)
        UserSession(user_id, ses_id)
        return ses_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returnd thr user_id based on the session id """
        user_obj = UserSession.search({'session_id': session_id}).to_json()
        return user_obj.get('user_id')

    def destroy_session(self, request=None) -> bool:
        """ destroy the user session instance in the db """
        return super().destroy_session(request)
