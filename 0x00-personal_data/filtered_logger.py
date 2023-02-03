#!/usr/bin/env python3
"""
    filtered_logger mod
"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ returns the log message obfuscated """
    for field in fields:
        regex = r'{}=(.*){}.*'.format(field, separator)
        spot = re.findall(regex, message)
        message = re.sub(spot[0].split(separator)[0], redaction, message)
    return message
