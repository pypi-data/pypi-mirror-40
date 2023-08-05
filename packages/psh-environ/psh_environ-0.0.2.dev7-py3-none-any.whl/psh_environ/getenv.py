# -*- coding: utf-8 -*-
"""
Fetch an environment variable and 🎉
"""

import os

from .decoder import decode_base64_json

UNDEFINED = object()

WELL_KNOWN_BASE64_JSON_VARIABLES = (
    "PLATFORM_APPLICATION",
    "PLATFORM_VARIABLES",
    "PLATFORM_RELATIONSHIPS",
    "PLATFORM_ROUTES",
)


def getenv(name, default=UNDEFINED, decode=None):
    if decode is None:
        decode = name in WELL_KNOWN_BASE64_JSON_VARIABLES

    try:
        value = os.environ[name]
    except KeyError:
        if default is UNDEFINED:
            raise
        else:
            return default

    if decode:
        value = decode_base64_json(value)

    return value
