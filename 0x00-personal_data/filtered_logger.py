#!/usr/bin/env python3
"""Obfuscates fields in log messages"""

import logging
import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Obfuscates `fields` in `message` with `redaction`

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


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.redact_fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Redacts log message fields


        Args:
            record (logging.LogRecord): line to redact

        Returns:
            str: Redacted log line
        """
        logline = super().format(record)
        return filter_datum(
            fields=self.redact_fields,
            redaction=self.REDACTION,
            message=logline,
            separator=self.SEPARATOR,
        )
