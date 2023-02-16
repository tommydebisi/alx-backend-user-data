#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
            Saves the user to the db and returns the User
            instance
        """
        user_inst = User(email=email, hashed_password=hashed_password)
        self._session.add(user_inst)
        self._session.commit()
        return user_inst

    def find_user_by(self, **kwargs) -> User:
        """
            searches and gets the user by the value passed from kwargs
            and return the first row
        """
        # check if kwarg is in the user dict
        if list(kwargs.keys())[0] not in list(User.__dict__.keys()):
            raise InvalidRequestError

        row = self._session.query(User).filter_by(**kwargs).first()
        if not row:
            raise NoResultFound
        return row

    def update_user(self, user_id: int, **kwargs) -> None:
        """
            Updates user with user_id with the key-value provided
            in kwargs
        """
        # find user by id first
        try:
            user_inst = self.find_user_by(id=user_id)
        except (InvalidRequestError, NoResultFound):
            return

        for key, val in kwargs.items():
            if list(kwargs.keys())[0] not in list(user_inst.__dict__.keys()):
                raise ValueError

            user_inst.__dict__[key] = val
            self.__session.commit()
