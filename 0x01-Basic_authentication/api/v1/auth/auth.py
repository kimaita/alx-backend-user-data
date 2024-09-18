#!/usr/bin/env python3
"""Implements API HTTP authentication"""

from flask import request
from typing import List, TypeVar
from pathlib import PurePath


class Auth:
    """Contains methods for handling API authentication"""

    def __init__(self):
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Defines routes that require authentication

        Returns:
            True if auth required, False otherwise
        """
        if not path or not excluded_paths:
            return True

        path += "/" if not path.endswith("/") else ""

        return all(not PurePath(path).match(excl) for excl in excluded_paths)

    def authorization_header(self, request=None) -> str:
        """Returns the request's `Authorization Header` or None"""
        if not request:
            return None

        auth = request.authorization

        return str(auth) if auth else None

    def current_user(self, request=None) -> TypeVar("User"):
        """Returns None"""
        return None
