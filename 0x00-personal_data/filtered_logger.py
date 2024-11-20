#!/usr/bin/env python3
"""Obfuscates fields in log messages"""

from typing import List
import re


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Obfuscates `fields` in message with `redaction`

    Args:
        fields (List[str]): fields in log line to obfuscate
        redaction (str): replacement text
        message (str): log line
        separator (str): field separator in the log line

    Returns:
        str: obfuscated message
    """
    pattern = re.compile(f"({'|'.join(fields)})=([^{separator}]*)")
    return re.sub(pattern, f"\\1={redaction}", message)
