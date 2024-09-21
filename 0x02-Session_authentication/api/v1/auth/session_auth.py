#!/usr/bin/env python3
"""Session Authentication module"""

from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """Implements session authentication"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session for a given user

        Return:
            str - the session ID
        """

        if isinstance(user_id, str):
            sess_id = str(uuid.uuid4())
            self.user_id_by_session_id[sess_id] = user_id
            return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""
        if isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User based on a cookie"""
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        if user_id:
            return User.get(user_id)

    def destroy_session(self, request=None):
        """Deletes a user session"""
        if not request:
            return False

        sess_cookie = self.session_cookie(request)
        if not sess_cookie:
            return False
        user_id = self.user_id_for_session_id(sess_cookie)
        if not user_id:
            return False

        del self.user_id_by_session_id[sess_cookie]
        return True
