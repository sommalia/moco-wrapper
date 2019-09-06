#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `moco_wrapper` package."""
import pytest
from moco_wrapper.moco_wrapper import Moco
from fixtures import moco, project_id
from click.testing import CliRunner

@pytest.fixture
def schedule_id(moco: Moco, project_id):
    response = moco.Schedule.getlist()
    entries = response.json()
    entry_id = -1
    if len(entries) == 0:
        response = moco.Schedule.create("2019-10-10", project_id=project_id)
        entry_id = response.json()["id"]
    else:
        entry_id = entries[-1]["id"]

    return entry_id



def test_schedule_create(moco: Moco, project_id):
    response = moco.Schedule.create("2019-10-10", project_id=project_id)
    print (response.content)
    assert response.status_code == 200

def test_schedule_update(moco: Moco, schedule_id, project_id):
    response = moco.Schedule.update(schedule_id, comment="test")
    print(response.content)
    assert response.status_code == 200

def test_schedule_get(moco: Moco, schedule_id):
    response = moco.Schedule.get(schedule_id)
    print(response.content)
    assert response.status_code == 200

def test_schedule_getlist(moco: Moco):
    response = moco.Schedule.getlist()
    print (response.content)
    assert response.status_code == 200

def test_schedule_delete(moco: Moco, schedule_id):
    response = moco.Schedule.delete(schedule_id)
    print (response.content)
    assert response.status_code == 200