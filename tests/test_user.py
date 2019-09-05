#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `moco_wrapper` package."""

from const import TEST_API_KEY, TEST_DOMAIN

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
    moco = Moco(api_key=TEST_API_KEY, domain=TEST_DOMAIN)
    return moco

@pytest.fixture
def unit_id():
    moco = Moco(api_key=TEST_API_KEY, domain=TEST_DOMAIN)
    return moco.Unit.getlist().json()[0]["id"]
    

@pytest.fixture
def user_id(unit_id):
    moco = Moco(api_key=TEST_API_KEY, domain=TEST_DOMAIN)
    users = moco.User.getlist().json()
    if len(users) > 1:
        return users[-1]["id"]
    else:
        user = moco.User.create("john", "doe", "testitest@byom.de", "init12345.", unit_id).json()
        return user["id"]

def test_user_create(moco: Moco, unit_id):
    response = moco.User.create("user created by", "test", "usercreatedbytest@byom.de", "init12345.", unit_id)
    print(response.content)
    assert response.status_code == 200

def test_user_update(moco: Moco, user_id):
    response = moco.User.update(user_id, firstname="jane", lastname="daws")
    print(response.content)
    assert response.status_code == 200

def test_user_get(moco: Moco, user_id):
    response = moco.User.get(user_id)
    print(response.content)
    assert response.status_code == 200

def test_user_getlist(moco: Moco):
    response = moco.User.getlist()
    print(response.content)
    assert response.status_code == 200

def test_user_delete(moco: Moco, user_id):
    response = moco.User.delete(user_id)
    assert response.status_code == 204