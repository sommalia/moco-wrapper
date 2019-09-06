import pytest
from moco_wrapper.moco_wrapper import Moco
from const import TEST_API_KEY, TEST_DOMAIN
import string
from random import randint, choice


@pytest.fixture(scope="session")
def moco():
    """return the moco object"""
    moco = Moco(api_key=TEST_API_KEY, domain=TEST_DOMAIN)
    return moco

@pytest.fixture(scope="session")
def project_id(moco: Moco):
    """return a single project id."""
    projects = moco.Project.getlist().json()
    return projects[0]["id"]

    
@pytest.fixture(scope="session")
def project_ids(moco: Moco):
    """return a list of project ids."""
    projects = moco.Project.getlist().json()
    project_ids = [x["id"] for x in projects]
    return project_ids

@pytest.fixture(scope="session")
def customer_id(moco: Moco):
    customers = moco.Company.getlist(company_type="customer").json()
    if len(customers) > 1: #do not use the first company, cannot update it
        return customers[-1]["id"]
    else:
        customer = moco.Company.create("customer created by test", company_type="customer").json()
        return customer["id"]

@pytest.fixture
def random_string():
    min_char = 8
    max_char = 12
    allchar = string.digits
    rand = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
    return rand

@pytest.fixture
def user_id(moco: Moco, random_string):
    users = moco.User.getlist().json()
    if len(users) > 0:
        return users[-1]["id"]
    else:
        user = moco.User.create("john", "doe", "this-user-can-be-deleted+{}@byom.de".format(random_string), "init12345.", unit_id).json()
        return user["id"]

@pytest.fixture
def deletable_user_id(moco: Moco, unit_id, random_string):
    users = moco.User.getlist(sort_by="id", sort_order='asc').json()
    if len(users) > 1:
        return users[-1]["id"]
    else:
        user = moco.User.create("john", "doe", "this-user-can-be-deleted+{}@byom.de".format(random_string), "init12345.", unit_id).json()
        print(user)
        return user["id"]
