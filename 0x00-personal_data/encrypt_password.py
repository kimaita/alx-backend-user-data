#!/usr/bin/env python3
"""Password hashing"""

import bcrypt


def hash_passsword(password: str) -> bytes:
    """Returns a salted hash of `password`

    Args:
        password (str): password to hash

    Returns:
        bytes: salted, hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates that `password` matches `hashed_password`

    Args:
        hashed_password (bytes): password hash
        password (str): password string

    Returns:
        bool: True if a match, False otherwise
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
