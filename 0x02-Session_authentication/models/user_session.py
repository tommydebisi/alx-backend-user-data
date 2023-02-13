#!/usr/bin/env python3
"""
    user session module
"""
from models.base import Base


class UserSession(Base):
    """
        user sesion class
    """
    def __init__(self, *args: list, **kwargs: dict):
        """ constructor func """
        super().__init__(*args, **kwargs)
        self.user_id = str(kwargs.get('user_id'))
        self.session_id = str(kwargs.get('session_id'))
