#!/usr/bin/env python3
"""Implements API HTTP authentication"""

from typing import List, TypeVar
import os


class Auth:
    """Contains methods for handling API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Defines routes that require authentication

        Returns:
            True if auth required, False otherwise
        """
        if not path or not excluded_paths:
            return True

        path += "/" if not path.endswith("/") else ""

        for ep in excluded_paths:
            if ep == path or ep.endswith("*") and path.startswith(ep[:-1]):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Returns the request's `Authorization Header` or None"""

        if not request:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):
        """Returns None"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie from a request"""
        if not request:
            return

        _my_session_id = os.getenv("SESSION_NAME")
        if _my_session_id:
            return request.cookies.get(_my_session_id)
