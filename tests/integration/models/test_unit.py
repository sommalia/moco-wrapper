import pytest

from moco_wrapper.util.response import JsonResponse, ListingResponse

from .. import IntegrationTest

class TestUnit(IntegrationTest):

    def test_getlist(self):
        data = {}
        with self.recorder.use_cassette("TestUnit.test_getlist"):
            unit_getlist = self.moco.Unit.getlist()

            assert unit_getlist.response.status_code == 200

            assert isinstance(unit_getlist, ListingResponse)

            data = unit_getlist.items

        return data

    def test_get(self):
        unit_list = self.test_getlist()

        with self.recorder.use_cassette("TestUnit.test_get"):
            unit_get = self.moco.Unit.get(unit_list[0].id)

            assert unit_get.response.status_code == 200

            assert isinstance(unit_get, JsonResponse)

            
