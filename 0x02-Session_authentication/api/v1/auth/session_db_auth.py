#!/usr/bin/env python3
"""
    session database auth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth, request
from models.user_session import UserSession
from datetime import timedelta, datetime
from uuid import uuid4


class SessionDBAuth(SessionExpAuth):
    """
        session db class
    """

    def create_session(self, user_id: str = None) -> str:
        """
            creates and returns a new session id with expiration date
        """
        if user_id is None or type(user_id) != str:
            return None

        ses_id = str(uuid4())

        user_session_dic = {
            "user_id": user_id,
            "session_id": ses_id
        }
        user_ses = UserSession(**user_session_dic)
        user_ses.save()
        return ses_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returnd thr user_id based on the session id """
        user_obj = UserSession.search({"session_id": session_id})
        if not user_obj[0]:
            return None
        if self.session_duration <= 0:
            return user_obj[0].user_id

        creat_at = user_obj[0].created_at

        # calculate differencce in time
        total_time = creat_at + timedelta(seconds=self.session_duration)

        #  check if session id has expired by checking current time
        if total_time < datetime.utcnow():
            self.destroy_session(request)
            return None
        return user_obj[0].user_id

    def destroy_session(self, request=None) -> bool:
        """ destroy the user session instance in the db """
        ses_id = self.session_cookie(request)
        if not ses_id:
            return False

        # get the instance object
        user_obj = UserSession.search({"session_id": ses_id})
        if not user_obj[0]:
            return False

        user_obj[0].remove()
