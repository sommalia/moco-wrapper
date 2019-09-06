"""Tests for moco_wrapper schedule model package."""
import pytest
from moco_wrapper.moco_wrapper import Moco
from fixtures import moco, project_id
from click.testing import CliRunner

@pytest.fixture
def expense_id(moco: Moco):
    #get an expense that was not billed, we cannot changed thos
    expenses = [x for x in moco.ProjectExpense.getall().json() if x["billed"] == False]
    if len(expenses) > 0:
        return expenses[-1]["id"]
    else:
        expense = moco.ProjectExpense.create(project_id, "2019-10-10", "this is the expense title", 2, "test unit", 22, 22).json()
        return expense["id"]


def test_projectexpense_create(moco: Moco, project_id):
    response = moco.ProjectExpense.create(project_id, "2019-10-10", "this is the expense title", 2, "test unit", 22, 22)
    print (response.content)
    assert response.status_code == 200

def test_projectexpense_create_bulk(moco: Moco, project_id):
    data = [
        {
            "date": "2019-10-10",
            "title": "this is the first item in bulk creation",
            "quantity": 3,
            "unit": "first bulk",
            "unit_price": 11,
            "unit_cost": 9

        },
        {
            "date": "2019-11-11",
            "title": "this is the second item in bulk creation",
            "quantity": 4,
            "unit": "first bulk",
            "unit_price": 24,
            "unit_cost": 18
        }
    ]

    response = moco.ProjectExpense.create_bulk(project_id, data)
    print (response.content)
    assert response.status_code == 200

def test_projectexpense_get(moco: Moco, project_id, expense_id):
    response = moco.ProjectExpense.get(project_id, expense_id)
    print(response.content)
    assert response.status_code == 200

def test_projectexpenese_getall(moco: Moco):
    response = moco.ProjectExpense.getall()
    print(response.content)
    assert response.status_code == 200

def test_projectexpense_getlist(moco: Moco, project_id):
    response = moco.ProjectExpense.getlist(project_id)
    print(response.content)
    assert response.status_code == 200

def test_projectexpense_update(moco: Moco, project_id, expense_id):
    response = moco.ProjectExpense.update(project_id, expense_id, quantity=100)
    print (response.content)
    assert response.status_code == 200

def test_projectexpense_disregard(moco: Moco, project_id, expense_id):
    response = moco.ProjectExpense.disregard(project_id, [expense_id], "disregarded by test")
    print(response.content)
    assert response.status_code
    