#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for moco_wrapper company model."""

import pytest
from moco_wrapper.moco_wrapper import Moco
from fixtures import moco, customer_id
from click.testing import CliRunner



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


