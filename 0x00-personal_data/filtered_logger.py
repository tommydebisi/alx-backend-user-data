#!/usr/bin/env python3
"""
    filtered_logger mod
"""
from typing import List
import re
import logging

PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'ip')


def get_logger() -> logging.Logger:
    """ returns the log obj """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    log = logging.StreamHandler(RedactingFormatter(PII_FIELDS))
    logger.addHandler(log)
    return logger


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ returns the log message obfuscated """
    for field in fields:
        regex = r'{}=.*?{}'.format(field, separator)
        repl_str = '{}={}{}'.format(field, redaction, separator)
        message = re.sub(regex, repl_str, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ returns filtered value from incoming log records """
        filtered = filter_datum(self.fields, self.REDACTION,
                                record.getMessage(), self.SEPARATOR)
        record.msg = filtered
        return super().format(record)
