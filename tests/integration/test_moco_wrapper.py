from . import IntegrationTest
import pytest

class TestMocoWrapper(IntegrationTest):
    
    def test_placeholder(self):
        print (pytest.placeholders)
        assert False