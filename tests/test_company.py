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
def customer_id():
    moco = Moco(api_key=TEST_API_KEY, domain=TEST_DOMAIN)
    customers = moco.Company.getlist(company_type="customer").json()
    if len(customers) > 1: #do not use the first company, cannot update it
        return customers[-1]["id"]
    else:
        customer = moco.Company.create("customer created by test", company_type="customer").json()
        return customer["id"]

def test_company_create(moco):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    response = moco.Company.create(name="created customer name", company_type="supplier")
    print (response.content)
    assert response.status_code == 200

def test_company_update(moco: Moco, customer_id):
    #760644958
    print(customer_id)
    response = moco.Company.update(customer_id, name="updated company name")
    print(response.content)
    assert response.status_code == 200

def test_company_get(moco: Moco, customer_id):
    response = moco.Company.get(customer_id)
    print(response.content)
    assert response.status_code == 200

def test_company_getlist(moco: Moco):
    response = moco.Company.getlist()
    print(response.content)
    assert response.status_code == 200


