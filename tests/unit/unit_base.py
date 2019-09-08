import pytest
from moco_wrapper.moco_wrapper import Moco
from moco_wrapper.util import TestRequester

class UnitTest(object):
    def setup(self):
        self.setup_moco()

    def setup_moco(self):
        """create a moco instance where no requests will be fired against the api"""
        self._moco = Moco(api_key="", domain="", http=TestRequester())

    @property
    def moco(self):
        return self._moco

    @property
    def requestor(self):
        return self._moco._requestor