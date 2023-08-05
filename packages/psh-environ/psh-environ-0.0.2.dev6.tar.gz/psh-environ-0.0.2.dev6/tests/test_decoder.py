# -*- coding: utf-8 -*-
import binascii
import sys  # noqa

import pytest
import simplejson as json
from psh_environ.decoder import decode_base64_json


@pytest.mark.parametrize(
    ("given", "expected"),
    [
        (b"eyJ0ZXN0IjogdHJ1ZX0K", {"test": True}),
        ("e30=", {}),
        (None, None),
        pytest.param(
            "invalid string",
            None,
            marks=(
                pytest.mark.xfail(
                    condition="sys.version_info < (3, 0)", raises=TypeError
                ),
                pytest.mark.xfail(
                    condition="sys.version_info >= (3, 0)", raises=binascii.Error
                ),
            ),
        ),
        pytest.param(
            "aW52YWxpZCBzdHJpbmc=",
            None,
            marks=pytest.mark.xfail(raises=json.JSONDecodeError),
        ),
    ],
)
def test_decode_base64_json(given, expected):
    actual = decode_base64_json(given)
    assert actual == expected
