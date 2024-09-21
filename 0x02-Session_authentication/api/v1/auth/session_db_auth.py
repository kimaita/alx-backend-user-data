#!/usr/bin/env python3
"""Persisted session authentication"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import uuid


class SessionDBAuth(SessionExpAuth):
    """"""

    def create_session(self, user_id=None):
        """Creates and stores a new user session

        Return:
            the session ID
        """
        if isinstance(user_id, str):
            sess_id = str(uuid.uuid4())
            user_sess = UserSession(user_id=user_id, session_id=sess_id)
            user_sess.save()
            return sess_id

    def user_id_for_session_id(self, session_id=None):
        """Returns a user ID associated a session ID"""
        try:
            user = UserSession.search({"session_id": session_id})[0]
            return user.id
        except Exception:
            return

    def destroy_session(self, request=None):
        """Destroys a user session associated with a request coookie"""
        if not request:
            return
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        user = UserSession.get(user_id)
        user.remove()

        return True
