#!/usr/bin/env python3
"""Implements authentication features"""

import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional


def _hash_password(password: str) -> bytes:
    """Hashes the given password using bcrypt

    Return:
         (bytes) salted hash of the password
    """
    if isinstance(password, str):
        hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hash


def _generate_uuid() -> str:
    """Returns a string uuid4"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Saves a user to the database.

        Return:
           the new User
        """
        try:
            u = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pwd = _hash_password(password)
            user = self._db.add_user(email, pwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Check the passed credentials against registered users

        Return:
            True if email exists with password
        """
        if isinstance(email, str) and isinstance(password, str):
            try:
                user = self._db.find_user_by(email=email)
                return bcrypt.checkpw(password.encode(), user.hashed_password)
            except Exception:
                return False

    def create_session(self, email: str) -> Optional[str]:
        """Creates a session for the user with the given email

        Return
            the session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """"""
        if not session_id:
            return

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return
