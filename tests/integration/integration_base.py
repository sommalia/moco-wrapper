import pytest
import betamax
import time
import string
import random

from datetime import date
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
        self.recorder = betamax.Betamax(self._moco.session)

    def setup_moco(self):
        self._moco = moco.Moco(
            pytest.placeholders.mocotest_apikey,
            pytest.placeholders.mocotest_domain,
            http=NoRetryRequestor())

    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        """
        create a radom string
        """
        return ''.join(random.choice(chars) for _ in range(size))

    def create_random_date(self):
        """
        presences can overlap so we are going to create a random date every time
        """
        return date(
            random.choice(range(2010, 2020, 1)),
            random.choice(range(1, 12, 1)),
            random.choice(range(1, 28))
        )

    @property
    def moco(self):
        return self._moco

    def teardown_method(self, method):
        """
        uncomment this if you need to generate everything, adds a delay between each test call
        """
        #time.sleep(5)
        pass