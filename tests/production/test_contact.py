#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for moco_wrapper model contact"""

import pytest
from moco_wrapper.moco_wrapper import Moco
from fixtures import moco
from click.testing import CliRunner

@pytest.fixture(scope="module")
def contact_id(moco):
    contact_id = -1
    contacts = moco.Contact.getlist().json()
    if len(contacts) == 0:
        contact = moco.Contact.create("t", "t", "F")
        contact_id = contact.json()["id"]
    else:
        contact_id = contacts[0]["id"]

    return contact_id

def test_contact_create(moco: Moco):
    response = moco.Contact.create("testfirstname", "testlastname", "M")
    print(response.content)
    assert response.status_code == 200

def test_contact_update(moco: Moco, contact_id):
    response = moco.Contact.update(contact_id, firstname="updated firstname")
    print(response.content)
    assert response.status_code == 200


def test_contact_get(moco: Moco, contact_id):
    response = moco.Contact.get(contact_id)
    print(response.content)
    assert response.status_code == 200

def test_contact_getlist(moco: Moco):
    response = moco.Contact.getlist()
    print(response.content)
    assert response.status_code == 200