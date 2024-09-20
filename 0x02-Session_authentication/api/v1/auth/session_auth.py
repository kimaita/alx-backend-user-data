#!/usr/bin/env python3
"""Session Authentication module"""

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Implements session authentication"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session for a given user

        Return:
            str - the session ID
        """

        if not isinstance(user_id, str):
            return None

        sess_id = str(uuid.uuid4())
        self.user_id_by_session_id[sess_id] = user_id
        return sess_id
