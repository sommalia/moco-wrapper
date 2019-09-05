#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `moco_wrapper` package."""

import pytest
from moco_wrapper.moco_wrapper import Moco

from click.testing import CliRunner

@pytest.fixture
def moco():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')
    moco = Moco(api_key="0ce6832b47a362994b5c07a21b958f3a", domain="asdf")
    return moco

def test_create(moco):
    #760644958
    response = moco.Unit.create(name="hier steht jetzt ganz anderer text")
    print(response.content)
    assert response.status_code == 200
