#!/usr/bin/env python3
"""A module that filter logs"""
import logging
from typing import List
import re
import mysql.connector
import os


pattern = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """It  returns the log message obfuscated"""
    ext, rep = (pattern['extract'], pattern['replace'])
    return re.sub(ext(fields, separator), rep(redaction), message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """It  returns the log message obfuscated"""
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt


def get_logger() -> logging.Logger:
    """It  returns a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    S_handler = logging.StreamHandler()
    S_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(S_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """"It connects to the database"""
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")

    db_connection = mysql.connector.connect(host=db_host, database=db_name,
                                            user=db_user, password=db_pwd)
    return db_connection


def main():
    """A  function that takes no arguments and returns nothing"""
    fields = 'name, email, phone, ssn, password, ip, last_login, user_agent'
    col = fields.split(',')
    query = 'SELECT {} FROM users;'.format(fields)
    logger = get_logger()
    connection = get_db()
    with connection.cursor() as curs:
        curs.execute(query)
        rows = curs.fetchall()
        for r in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(col, r)
            )
            msg = '{};'.format(';'.join(list(record)))
            args = ('user_date', logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            logger.handle(log_record)


if __name__ == '__main__':
    main()
