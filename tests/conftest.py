import pytest
import os

environment_keys = [
    "mocotest_apikey",
    "mocotest_domain"
]

placeholders = {
    "test_placeholder" : "this is a test placeholder"
} 

##init placeholders from environment
for key in environment_keys:
    placeholders[key] = os.environ.get(key) 

class Placeholders(object):
    def __init__(self, _dict):
        self.__dict__ = _dict

def pytest_configure():
    pytest.placeholders = Placeholders(placeholders)