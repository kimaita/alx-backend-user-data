#!/usr/bin/env python3
"""Expiration for authenticated session"""

import os
from api.v1.auth.session_auth import SessionAuth
from typing import Optional
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Implements session expiration"""

    def __init__(self):
        try:
            duration = int(os.getenv("SESSION_DURATION", 0))
        except Exception:
            duration = 0

        self.session_duration = duration

    def create_session(self, user_id=None) -> Optional[str]:
        """Creates a session

        Return
            the session ID
        """
        sess_id = super().create_session(user_id)
        if not sess_id:
            return
        self.user_id_by_session_id[sess_id] = {
            "user_id": user_id,
            "created_at": datetime.now(),
        }
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """Returns a User ID based on a Session ID"""
        if not session_id:
            return

        user_sess = self.user_id_by_session_id.get(session_id)
        if not user_sess:
            return

        if self.session_duration <= 0:
            return user_sess["user_id"]

        created = user_sess.get("created_at")
        if not created:
            return

        expiry = created + timedelta(seconds=self.session_duration)
        if expiry <= datetime.now():
            return None
        return user_sess["user_id"]
