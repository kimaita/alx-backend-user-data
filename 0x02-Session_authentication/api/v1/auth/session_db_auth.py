#!/usr/bin/env python3
"""Persisted session authentication"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
import uuid


class SessionDBAuth(SessionExpAuth):
    """Manages persisted session data"""

    def __init__(self):
        super().__init__()

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

    def user_id_for_session_id(self, session_id: str = None):
        """Returns a user ID associated a session ID"""

        try:
            user_sess = UserSession.search({"session_id": session_id})[0]
        except Exception:
            return

        if self.session_duration <= 0:
            return user_sess.user_id

        created = user_sess.created_at
        if not created:
            return

        expiry = created + timedelta(seconds=self.session_duration)
        if expiry <= datetime.utcnow():
            return None

        return user_sess.user_id

    def destroy_session(self, request=None):
        """Destroys a user session associated with a request cookie"""
        if not request:
            return
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        sess = UserSession.get(user_id)
        sess.remove()

        return True
