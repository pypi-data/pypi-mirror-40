# -*- coding: utf-8 -*-
import pytest
from psh_environ.getenv import getenv


def test_getenv_nokey_nodefault(monkeypatch):
    monkeypatch.delenv("PATH")
    with pytest.raises(KeyError):
        getenv("PATH")


def test_getenv_nokey_default(monkeypatch):
    monkeypatch.delenv("PATH")
    default = object()
    assert getenv("PATH", default) is default


def test_getenv_explicit_decode(monkeypatch):
    monkeypatch.setenv("PATH", "e30=")
    assert getenv("PATH", decode=True) == {}


def test_getenv_wellknown(monkeypatch):
    monkeypatch.setenv("PLATFORM_VARIABLES", "e30=")
    assert getenv("PLATFORM_VARIABLES") == {}


def test_getenv_wellknown_explicit_no_decode(monkeypatch):
    monkeypatch.setenv("PLATFORM_VARIABLES", "e30=")
    assert getenv("PLATFORM_VARIABLES", decode=False) == "e30="
