#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for moco_wrapper model comment."""
import pytest
from fixtures import moco, project_id, project_ids
from moco_wrapper.moco_wrapper import Moco
        
@pytest.fixture()
def comment_id(moco: Moco):
    """return a comment id"""
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

