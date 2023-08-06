# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

""" util.py for utilities"""
import logging
import datetime
import dateutil.parser
import json
import base64
import six


def _parse_expiry_time_from_token(token):
    payload = token.split(".")[1]
    missing_padding = len(payload) % 4
    if missing_padding:
        payload += '=' * (4 - missing_padding)
    decoded_payload = base64.b64decode(payload.encode('utf-8'))
    if isinstance(decoded_payload, six.binary_type):
        decoded_payload = decoded_payload.decode('utf-8')
    payload_dict = json.loads(decoded_payload)
    return _parse_date(payload_dict['exp'])


def _parse_date(expiry_time):
    if isinstance(expiry_time, datetime.datetime):
        return expiry_time
    try:
        date = dateutil.parser.parse(expiry_time)
    except (ValueError, TypeError):
        date = datetime.datetime.fromtimestamp(int(expiry_time))
    return date


class NewLoggingLevel(object):
    """
    A class for setting up logging levels.
    """
    def __init__(self, logger_name, level=logging.WARNING):
        """
        :param logger_name:
        :type logger_name: str
        :param level:
        :type level: int
        """
        self.logger_name = logger_name
        self.logger = logging.getLogger(logger_name)
        self.old_level = self.logger.level
        self.new_level = level

    def __enter__(self):
        """
        :return: logger
        :rtype: RootLogger
        """
        self.logger.setLevel(self.new_level)
        return self.logger

    def __exit__(self, et, ev, tb):
        """
        :param et: Exception type
        :type et:
        :param ev: Exception value
        :type ev:
        :param tb: Traceback
        :type tb:
        """
        self.logger.setLevel(self.old_level)
