import pytest
import betamax

from moco_wrapper.moco_wrapper import Moco

class IntegrationTest(object):
    """Base class for integration tests."""

    def setup(self):
        self.setup_moco()
        self.setup_betamax()

    def setup_betamax(self):
        self.recorder = betamax.Betamax(self._moco.http)

    def setup_moco(self):
        self._moco = Moco(pytest.placeholders.mocotest_apikey, pytest.placeholders.mocotest_domain)

    @property
    def moco(self):
        return self._moco