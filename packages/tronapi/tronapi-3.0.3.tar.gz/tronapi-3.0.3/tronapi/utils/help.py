# --------------------------------------------------------------------
# Copyright (c) iEXBase. All rights reserved.
# Licensed under the MIT License.
# See License.txt in the project root for license information.
# --------------------------------------------------------------------
import platform
import re
from typing import Any

import base58
import tronapi


def format_user_agent(name=None):
    """Construct a User-Agent suitable for use in client code.
    This will identify use by the provided ``name`` (which should be on the
    format ``dist_name/version``), TronAPI version and Python version.
    .. versionadded:: 1.1
    """
    parts = ['TronAPI/%s' % tronapi.__version__,
             '%s/%s' % (platform.python_implementation(),
                        platform.python_version())]
    if name:
        parts.insert(0, name)
    return ' '.join(parts)


def string_utf8_to_hex(name):
    return bytes(name, encoding='utf-8').hex()


def hex_to_base58(value: Any) -> str:
    return base58.b58encode_check(bytes.fromhex(value))


def is_valid_url(value):
    """Return whether or not given value is a valid URL.

    Args:
        value(str): URL address string to validate
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    result = regex.match(value)
    return bool(result)
