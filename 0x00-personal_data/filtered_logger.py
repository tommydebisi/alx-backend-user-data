#!/usr/bin/env python3
"""
    filtered_logger mod
"""
from typing import List
import re
import logging
import mysql.connector
from os import getenv

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ returns a connector to the database """
    user = getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    passwd = getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db = getenv('PERSONAL_DATA_DB_NAME')
    return mysql.connector.connect(host=host, password=passwd,
                                   user=user, database=db)


def get_logger() -> logging.Logger:
    """ returns the log obj """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False  # this logger is the root logger

    # provide where to log the output to
    stream = logging.StreamHandler()
    stream.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream)
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

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ returns filtered value from incoming log records """
        filtered = filter_datum(self.fields, self.REDACTION,
                                record.getMessage(), self.SEPARATOR)
        record.msg = filtered
        return super().format(record)


def main() -> None:
    """ filters rows from the db """
    connect = get_db()
    cursor = connect.cursor()

    logger = get_logger()
    cols = ['name', 'email', 'phone', 'ssn',
            'password', 'ip', 'last_login', 'user_agent']
    cursor.execute('SELECT * FROM users;')
    for row in cursor:
        message = ""
        for name, val in zip(cols, row):
            message += '{}={};'.format(name, val)
        logger.info(message)

    cursor.close()
    connect.close()


if __name__ == "__main__":
    main()
