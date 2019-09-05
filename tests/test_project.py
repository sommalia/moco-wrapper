#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `moco_wrapper` package."""

from const import TEST_API_KEY, TEST_DOMAIN, KNOWN_CUSTOMER_ID, KNOWN_PROJECT_ID, KNOWN_USER_ID
import pytest
from moco_wrapper.moco_wrapper import Moco

from click.testing import CliRunner




@pytest.fixture(scope="module")
def moco():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')
    moco = Moco(api_key=TEST_API_KEY, domain=TEST_DOMAIN)
    return moco

@pytest.fixture(scope="module")
def user_id(moco):
    users = moco.User.getlist().json()
    return users[0]["id"]

@pytest.fixture(scope="module")
def customer_id(moco):
    customers = moco.Company.getlist(company_type="customer").json()
    return customers[0]["id"]

@pytest.fixture(scope="module")
def project_id(moco):
    projects = moco.Project.getlist().json()
    return projects[-1]["id"]
    

def test_project_create(moco: Moco, user_id, customer_id):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    response = moco.Project.create("testproject", "EUR", "2019-10-10", user_id, customer_id)
    print (response.content)
    assert response.status_code == 200

def test_project_update(moco: Moco, project_id):
    response = moco.Project.update(project_id, name="this is the updated name")
    print (response.content)
    assert response.status_code == 200

def test_project_get(moco: Moco, project_id):
    response = moco.Project.get(project_id)
    print (response.content)
    assert response.status_code == 200

def test_project_getlist(moco: Moco):
    response = moco.Project.getlist()
    print (response.content)
    assert response.status_code == 200

def test_project_archive(moco: Moco, project_id):
    response = moco.Project.archive(project_id)
    print (response.content)
    assert response.status_code == 200

def test_project_unarchive(moco: Moco, project_id):
    response = moco.Project.unarchive(project_id)
    print (response.content)
    assert response.status_code == 200

def test_project_report(moco: Moco, project_id):
    response = moco.Project.report(project_id)
    print(response.content)
    assert(response.status_code)