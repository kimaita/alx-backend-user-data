#!/usr/bin/env python3
"""Basic HTTP Authentication"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Defines methods for implemmenting HTTP Authentication"""

    def extract_base64_authorization_header(
        self,
        authorization_header: str,
    ) -> str:
        """Returns the Base64 part of the Authorization header
        for Basic Authentication"""

        if authorization_header and isinstance(authorization_header, str):
            tag = "Basic "
            if authorization_header.startswith(tag):
                return authorization_header[len(tag):]

        return None
