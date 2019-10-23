import pytest
import os
import betamax

from betamax_serializers import pretty_json

placeholders = {
    "test_placeholder" : "this is a test placeholder"
} 

##init placeholders from environment
placeholders["mocotest_apikey"] = os.environ.get("mocotest_apikey", "test_api_key")
placeholders["mocotest_domain"] = os.environ.get("mocotest_domain", "test_domain")


class Placeholders(object):
    def __init__(self, _dict):
        self.__dict__ = _dict

def pytest_configure():
    pytest.placeholders = Placeholders(placeholders)

betamax.Betamax.register_serializer(pretty_json.PrettyJSONSerializer)
with betamax.Betamax.configure() as config:
    config.cassette_library_dir = "tests/integration/cassettes"
    config.default_cassette_options["serialize_with"] = "prettyjson"
    config.default_cassette_options["match_requests_on"] = ["path", "method"]