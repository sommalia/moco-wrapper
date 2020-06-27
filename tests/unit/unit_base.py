import pytest
import string
import random

from moco_wrapper import moco
from moco_wrapper.util.requestor import RawRequestor
from moco_wrapper.util.objector import RawObjector


class UnitTest(object):
    def setup(self):
        self.setup_moco()

    def setup_moco(self):
        """create a moco instance where no requests will be fired against the api"""
        self._moco = moco.Moco(
            auth={
                "api_key": "<TOKEN>",
                "domain": "<DOMAIN>"
            },
            requestor=RawRequestor(),
            objector=RawObjector()
        )

    @property
    def moco(self):
        return self._moco

    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        """
        create a random string
        """
        return ''.join(random.choice(chars) for _ in range(size))
