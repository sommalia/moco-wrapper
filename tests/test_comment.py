#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `moco_wrapper` package."""

from const import TEST_API_KEY, TEST_DOMAIN, KNOWN_USER_ID, KNOWN_PROJECT_ID

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
def project_id():
    moco = Moco(api_key=TEST_API_KEY, domain=TEST_DOMAIN)
    projects = moco.Project.getlist().json()
    return projects[0]["id"]

@pytest.fixture
def project_ids():
    moco = Moco(api_key=TEST_API_KEY, domain=TEST_DOMAIN)
    projects = moco.Project.getlist().json()
    project_ids = [x["id"] for x in projects]
    return project_ids

@pytest.fixture
def comment_id():
    moco = Moco(api_key=TEST_API_KEY, domain=TEST_DOMAIN)
    comments = moco.Comment.getlist().json()

    if len(comments) > 0:
        return comments[0]["id"]
    else:
        comment = moco.Comment.create(project_id(), "Project", "comment created for fix").json()
        return comment["id"]
        


def test_comment_create_single(moco: Moco, project_id):
    response = moco.Comment.create(project_id, "Project", "created single comment")
    print (response.content)
    assert response.status_code == 200

def test_comment_create_bulk(moco: Moco, project_ids):
    response = moco.Comment.create_bulk(project_ids, "Project", "created bulk comment")
    print(response.content)
    assert response.status_code == 200

def test_comment_update(moco: Moco, comment_id):
    response = moco.Comment.update(comment_id, "hier steht jetzt ein neuer comment")
    print(response.content)
    assert response.status_code == 200

def test_comment_get(moco: Moco, comment_id):
    response = moco.Comment.get(comment_id)
    print(response.status_code)
    assert response.status_code == 200

def test_comment_getlist(moco: Moco):
    response = moco.Comment.getlist()
    print(response.content)
    assert response.status_code == 200

def test_comment_delete(moco: Moco, comment_id):
    response = moco.Comment.delete(comment_id)
    print(response.content)
    assert response.status_code == 204

