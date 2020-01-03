import pytest

from moco_wrapper.util.response import JsonResponse, ListingResponse

from .. import IntegrationTest

class TestUnit(IntegrationTest):

    def test_getlist(self):
        data = {}
        with self.recorder.use_cassette("TestUnit.test_getlist"):
            response = self.moco.Unit.getlist()
            assert isinstance(response, ListingResponse)
            data = response.items

        return data

    def test_get(self):
        unit_list = self.test_getlist()

        with self.recorder.use_cassette("TestUnit.test_get"):
            response = self.moco.Unit.get(unit_list[0].id)
            assert isinstance(response, JsonResponse)

            
