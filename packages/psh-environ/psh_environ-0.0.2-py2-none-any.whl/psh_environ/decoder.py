# -*- coding: utf-8 -*-
import base64

import simplejson as json


def decode_base64_json(string):
    if string is None:
        return None

    if hasattr(string, "encode"):
        string = string.encode("ascii")

    return json.loads(base64.b64decode(string))
