from . import IntegrationTest
import pytest

class TestMocoWrapper(IntegrationTest):
    
    def test_placeholder(self):
        assert pytest.placeholders.test_placeholder is not None

    def test_environ_api_key(self):
        print ("set mocotest_apikey environment variable")
        print ("> export mocotest_apikey=\"<TOKEN>\"")
        assert pytest.placeholders.mocotest_apikey is not None

    def test_environ_domain(self):
        print ("set mocotest_domain environment variable")
        print ("> export mocotest_domain=\"<DOMAIN>\"")
        assert pytest.placeholders.mocotest_domain is not None

    