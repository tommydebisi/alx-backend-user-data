#!/usr/bin/env python3
"""
    Session Expiration Module
"""
from api.v1.auth.session_auth import SessionAuth, request
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
        Session Expiration class
    """
    def __init__(self) -> None:
        """ constructor func """
        self.session_duration = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id: str = None) -> str:
        """ returns session id and set value of user id and current to it """
        ses_id = super().create_session(user_id)
        if ses_id is None:
            return None

        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[ses_id] = session_dictionary
        return ses_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
            returns user id related with session id provided it has
            not expired6
        """
        if session_id is None:
            return None

        ses_dic = self.user_id_by_session_id.get(session_id)
        if ses_dic is None:
            return None

        if self.session_duration <= 0:
            return ses_dic.get('user_id')

        creat_at = ses_dic.get('created_at')
        if creat_at is None:
            return None

        # calculate differencce in time
        total_time = creat_at + timedelta(seconds=self.session_duration)

        #  check if session id has expired by checking current time
        if total_time < datetime.now():
            return None
        return ses_dic.get('user_id')
