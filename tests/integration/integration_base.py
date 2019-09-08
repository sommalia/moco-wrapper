import pytest
from moco_wrapper.moco_wrapper import Moco

class IntegrationTest(object):
    """Base class for integration tests."""

    def setup(self):
        self.setup_moco()
        self.setup_betamax()

    def setup_betamax(self):
        self.recorder = Betamax(self._moco._session)

    def setup_moco(self):
        self._moco = Moco()
