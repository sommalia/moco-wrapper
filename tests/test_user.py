#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for moco_wrapper model user."""

import pytest
from moco_wrapper.moco_wrapper import Moco
from fixtures import moco, deletable_user_id, user_id, random_string
from click.testing import CliRunner


@pytest.fixture(scope="module")
def unit_id(moco):
    return moco.Unit.getlist().json()[0]["id"]
    

def test_user_create(moco: Moco, unit_id, random_string):
    response = moco.User.create("user created by", "test", "usercreatedbytest+{}@byom.de".format(random_string), "init12345.", unit_id)
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

def test_user_delete(moco: Moco, deletable_user_id):
    response = moco.User.delete(deletable_user_id)
    print(response.content)
    assert response.status_code == 204