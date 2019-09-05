#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `moco_wrapper` package."""

from const import TEST_API_KEY, TEST_DOMAIN, KNOWN_CUSTOMER_ID

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

def test_company_create(moco):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    response = moco.Company.create(name="hier stehen jetzt noch mehr zeichen", company_type="supplier")
    print (response.content)
    assert response.status_code == 200

def test_company_update(moco):
    #760644958
    response = moco.Company.update(KNOWN_CUSTOMER_ID, name="hier steht jetzt ganz anderer text")
    print(response.content)
    assert response.status_code == 200

def test_company_get(moco):
    response = moco.Company.get(KNOWN_CUSTOMER_ID)
    print(response.content)
    assert response.status_code == 200

def test_company_getlist(moco):
    response = moco.Company.getlist()
    print(response.content)
    assert response.status_code == 200
