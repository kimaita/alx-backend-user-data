#!/usr/bin/env python3
"""Basic HTTP Authentication"""

from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """Defines methods for implemmenting HTTP Authentication"""

    def extract_base64_authorization_header(
        self,
        authorization_header: str,
    ) -> str:
        """Returns the Base64 part of the Authorization header
        for Basic Authentication"""

        if isinstance(authorization_header, str):
            tag = "Basic "
            if authorization_header.startswith(tag):
                return authorization_header[len(tag):]

        return None

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str,
    ) -> str:
        """Decodes a base64 string"""
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            auth = base64.b64decode(base64_authorization_header)
            return auth.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """Returns the user email and password from the Base64 decoded value.
        Returns
            (email, password)
        """
        email, pwd = None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return email, pwd

        try:
            email, pwd = decoded_base64_authorization_header.split(":")
        except Exception:
            pass

        return email, pwd

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str,
    ) -> TypeVar("User"):
        """Retrieves a user given some credentials"""
        if not (isinstance(user_email, str) and isinstance(user_pwd, str)):
            return None

        users = User.search({"email": user_email})
        if not users:
            return None

        user = users[0]
        if user.is_valid_password(user_pwd):
            return user
        return None
