import pytest

from moco_wrapper.util.response import JsonResponse

from .. import IntegrationTest

class TestUser(IntegrationTest):

    def test_create(self):


        with self.recorder.use_cassette("TestUser.test_create"):
            unit = self.moco.Unit.getlist()
            unit_id = unit.items[0].id

            response = self.moco.User.create("testfirstname", "testlastname", "email@email.de", "password", unit_id)

            assert isinstance(response, JsonResponse)