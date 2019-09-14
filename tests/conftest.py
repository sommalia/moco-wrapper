import pytest
import os

placeholders = {
    "test_placeholder" : "this is a test placeholder"
} 

##init placeholders from environment
placeholders["mocotest_apikey"] = os.environ.get("mocotest_apikey", "[APIKEY]")
placeholders["mocotest_domain"] = os.environ.get("mocotest_domain", "[DOMAIN]")


class Placeholders(object):
    def __init__(self, _dict):
        self.__dict__ = _dict

def pytest_configure():
    pytest.placeholders = Placeholders(placeholders)