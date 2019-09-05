#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `moco_wrapper` package."""

from const import TEST_API_KEY, TEST_DOMAIN, KNOWN_CUSTOMER_ID, KNOWN_PROJECT_ID, KNOWN_USER_ID
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

def test_project_create(moco: Moco):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    response = moco.Project.create("testproject", "EUR", "2019-10-10", KNOWN_USER_ID, KNOWN_CUSTOMER_ID )
    print (response.content)
    assert response.status_code == 200

def test_project_update(moco: Moco):
    response = moco.Project.update(KNOWN_PROJECT_ID, name="this is the updated name")
    print (response.content)
    assert response.status_code == 200

def test_project_get(moco: Moco):
    response = moco.Project.get(KNOWN_PROJECT_ID)
    print (response.content)
    assert response.status_code == 200

def test_project_getlist(moco: Moco):
    response = moco.Project.getlist()
    print (response.content)
    assert response.status_code == 200

def test_project_archive(moco: Moco):
    response = moco.Project.archive(KNOWN_PROJECT_ID)
    print (response.content)
    assert response.status_code == 200

def test_project_unarchive(moco: Moco):
    response = moco.Project.unarchive(KNOWN_PROJECT_ID)
    print (response.content)
    assert response.status_code == 200

def test_project_report(moco: Moco):
    response = moco.Project.report(KNOWN_PROJECT_ID)
    print(response.content)
    assert(response.status_code)