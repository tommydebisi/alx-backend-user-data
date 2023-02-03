#!/usr/bin/env python3
"""
    filtered_logger mod
"""
from typing import List
import re


def getPattern(message: str, pattern: str, separator: str) -> str:
    """ gets pattern needed to substitute """
    regex = r'{}=(.*){}.*'.format(pattern, separator)
    spot = re.findall(regex, message)
    return spot[0].split(separator)[0]


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ returns the log message obfuscated """
    for field in fields:
        pat = getPattern(message, field, separator)
        message = re.sub(pat, redaction, message)
    return message
