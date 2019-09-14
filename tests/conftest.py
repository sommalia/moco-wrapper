import pytest

placeholders = {
    "test_placeholder" : "best"
} 

class Placeholders(object):
    def __init__(self, _dict):
        self.__dict__ = _dict

def pytest_configure():
    pytest.placeholders = Placeholders(placeholders)