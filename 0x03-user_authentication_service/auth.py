#!/usr/bin/env python3
"""Implements authentication features"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes the given password using bcrypt

    Return:
         (bytes) salted hash of the password
    """
    if isinstance(password, str):
        hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hash


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
                if bcrypt.checkpw(password.encode(), user.hashed_password):
                    return True
                return False
            except Exception:
                return False
