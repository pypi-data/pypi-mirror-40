# -*- coding: utf-8 -*-

import pytest


def dict_parametrize(argnames, paramsdict, indirect=False, scope=None):
    """Decorator to parametrize test functions from a (id, argvalue) dict."""
    ids, argvalues = zip(*paramsdict.items())  # ensure id matches its argvalue
    return pytest.mark.parametrize(argnames, argvalues, indirect, ids, scope)
