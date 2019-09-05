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



def test_projectcontract_delete(moco: Moco):
    contract_id = -1
    contracts = moco.ProjectContract.getlist(KNOWN_PROJECT_ID).json()
    if len(contracts) == 0:
        created_contract = moco.ProjectContract.create(KNOWN_PROJECT_ID, KNOWN_USER_ID).json()
        contract_id = created_contract["id"]
    else:
        contract_id = contracts[0]["id"]

    response = moco.ProjectContract.delete(KNOWN_PROJECT_ID, contract_id)
    print(response.content)
    #status code is success, but no content
    assert response.status_code == 204

def test_projectcontract_create(moco: Moco):
    response = moco.ProjectContract.create(KNOWN_PROJECT_ID, KNOWN_USER_ID)
    print(response.content)
    assert response.status_code == 200


def test_projectcontract_update(moco: Moco):
    contract_id = -1
    contracts = moco.ProjectContract.getlist(KNOWN_PROJECT_ID).json()
    if len(contracts) == 0:
        created_contract = moco.ProjectContract.create(KNOWN_PROJECT_ID, KNOWN_USER_ID).json()
        contract_id = created_contract["id"]
    else:
        contract_id = contracts[0]["id"]

    response = moco.ProjectContract.update(KNOWN_PROJECT_ID, contract_id, budget=420)
    print (response.content)
    assert response.status_code == 200


def test_projectcontract_get(moco: Moco):
    contract_id = -1
    contracts = moco.ProjectContract.getlist(KNOWN_PROJECT_ID).json()
    if len(contracts) == 0:
        created_contract = moco.ProjectContract.create(KNOWN_PROJECT_ID, KNOWN_USER_ID).json()
        contract_id = created_contract["id"]
    else:
        contract_id = contracts[0]["id"]

    response = moco.ProjectContract.get(KNOWN_PROJECT_ID, contract_id)
    print (response.content)
    assert response.status_code == 200

def test_projectcontract_getlist(moco: Moco):
    response = moco.ProjectContract.getlist(KNOWN_PROJECT_ID)
    print (response.content)
    assert response.status_code == 200