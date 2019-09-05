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

def test_contact_create(moco: Moco):
    response = moco.Contact.create("testfirstname", "testlastname", "M")
    print(response.content)
    assert response.status_code == 200

def test_contact_update(moco: Moco):
    contact_id = -1
    contacts = moco.Contact.getlist().json()
    if len(contacts) == 0:
        contact = moco.Contact.create("t", "t", "F")
        contact_id = contact.json()["id"]
    else:
        contact_id = contacts[0]["id"]

    response = moco.Contact.update(contact_id, firstname="updated firstname")
    print(response.content)
    assert response.status_code == 200


def test_contact_get(moco: Moco):
    contact_id = -1
    contacts = moco.Contact.getlist().json()
    if len(contacts) == 0:
        contact = moco.Contact.create("t", "t", "F")
        contact_id = contact.json()["id"]
    else:
        contact_id = contacts[0]["id"]

    response = moco.Contact.get(contact_id)
    print(response.content)
    assert response.status_code == 200

def test_contact_getlist(moco: Moco):
    response = moco.Contact.getlist()
    print(response.content)
    assert response.status_code == 200