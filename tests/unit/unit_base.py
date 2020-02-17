import pytest
from moco_wrapper.moco_wrapper import Moco
from moco_wrapper.util.requestor import RawRequestor
from moco_wrapper.util.objector import RawObjector

class UnitTest(object):
    def setup(self):
        self.setup_moco()

    def setup_moco(self):
        """create a moco instance where no requests will be fired against the api"""
        self._moco = Moco(api_key="[HERE IS THE API KEY]", domain="[DOMAIN]", http=RawRequestor(), objector=RawObjector())

    @property
    def moco(self):
        return self._moco

    @property
    def requestor(self):
        return self._moco._requestor