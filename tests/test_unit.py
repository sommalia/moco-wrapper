#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for moco_wrapper model unit."""

import pytest
from moco_wrapper.moco_wrapper import Moco
from fixtures import moco
from click.testing import CliRunner

@pytest.fixture(scope="module")
def unit_id(moco):
    units = moco.Unit.getlist().json()
    return units[0]["id"]


def test_unit_get(moco: Moco, unit_id):
    response = moco.Unit.get(unit_id)
    print(response.content)
    assert response.status_code == 200

def test_unit_getlist(moco: Moco):
    response = moco.Unit.getlist()
    print(response.content)
    assert response.status_code == 200