#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `moco_wrapper` package."""

from const import TEST_API_KEY, TEST_DOMAIN
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
def customer_id():
    moco = Moco(api_key=TEST_API_KEY, domain=TEST_DOMAIN)
    customers = moco.Company.getlist(company_type="customer").json()
    if len(customers) > 1:
        return customers[-1]["id"]
    else:
        customer = moco.Company.create("company created by project contract test", company_type="customer").json()
        return customer["id"]

@pytest.fixture(scope="module")
def unit_id():
    moco = Moco(api_key=TEST_API_KEY, domain=TEST_DOMAIN)
    units = moco.Unit.getlist().json()
    return units[0]["id"]

@pytest.fixture(scope="module")
def user_id(unit_id):
    moco = Moco(api_key=TEST_API_KEY, domain=TEST_DOMAIN)
    users = moco.User.getlist().json()
    if len(users) > 1:
        return users[0]["id"]
    else:
        user = moco.User.create("user created by", "project contract test", "usercreatedbyprojectcontracttest@byom.de", "init12345.", unit_id).json()
        return user["id"]


@pytest.fixture(scope="module")
def project_id(user_id, customer_id):
    moco = Moco(api_key=TEST_API_KEY, domain=TEST_DOMAIN)
    project = moco.Project.create("project created for contract test", "EUR", "2019-10-10",user_id,customer_id).json()
    return project["id"]



def test_projectcontract_create(moco: Moco, project_id, user_id):
    response  = moco.ProjectContract.getlist(project_id)
    print(response.content)
    assert response.status_code == 200

    contracts = response.json()
    if len(contracts) > 0:
        for c in contracts:
            moco.ProjectContract.delete(project_id, c["id"])

    response = moco.ProjectContract.create(project_id, user_id)
    print(response.content)
    assert response.status_code == 200


def test_projectcontract_update(moco: Moco, project_id):
    contract_id = -1

    response = moco.ProjectContract.getlist(project_id)
    print (response.content)
    contracts = response.json()

    if len(contracts) == 0:
        response = moco.ProjectContract.create(project_id, user_id)
        print(response.content)
        contract_id = created_contract.json()["id"]
    else:
        contract_id = contracts[0]["id"]

    response = moco.ProjectContract.update(project_id, contract_id, budget=420)
    print (response.content)
    assert response.status_code == 200


def test_projectcontract_delete(moco: Moco, project_id):
    contract_id = -1
    contracts = moco.ProjectContract.getlist(project_id).json()
    if len(contracts) == 0:
        created_contract = moco.ProjectContract.create(project_id, user_id).json()
        contract_id = created_contract["id"]
    else:
        contract_id = contracts[0]["id"]


    response = moco.ProjectContract.delete(project_id, contract_id)
    print(response.content)
    #status code is success, but no content
    assert response.status_code == 204

def test_projectcontract_get(moco: Moco, project_id, user_id):
    contract_id = -1
    response = moco.ProjectContract.getlist(project_id)
    #print(response.content)
    assert response.status_code == 200
    contracts = list(response.json())

    if len(contracts) == 0:
        response = moco.ProjectContract.create(project_id, user_id)
        print(response.content)
        assert response.status_code == 200
        contract_id = response.json()["id"]
    else:
        contract_id = contracts[0]["id"]

    response = moco.ProjectContract.get(project_id, contract_id)
    print (response.content)
    assert response.status_code == 200

def test_projectcontract_getlist(moco: Moco, project_id):
    response = moco.ProjectContract.getlist(project_id)
    print (response.content)
    assert response.status_code == 200



