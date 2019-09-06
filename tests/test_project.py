#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for moco_wrapper model project"""
import pytest
from moco_wrapper.moco_wrapper import Moco
from fixtures import moco, user_id, customer_id, project_id
from click.testing import CliRunner


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