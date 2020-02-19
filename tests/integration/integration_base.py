import pytest
import betamax
import time

from moco_wrapper import moco
from moco_wrapper.util.requestor import NoRetryRequestor

class IntegrationTest(object):
    """Base class for integration tests.
    
    The Integration tests check if the requests that are created will be sent out correctly and can be parsed back into a real object
    
    """

    def setup(self):
        self.setup_moco()
        self.setup_betamax()

    def setup_betamax(self):
        self.recorder = betamax.Betamax(self._moco.http)

    def setup_moco(self):
        self._moco = moco.Moco(
            pytest.placeholders.mocotest_apikey,
            pytest.placeholders.mocotest_domain,
            http=NoRetryRequestor())

    @property
    def moco(self):
        return self._moco

    def teardown_method(self, method):
        """
        uncomment this if you need to generate everything, adds a delay between each test call
        """
        #time.sleep(5)
        pass