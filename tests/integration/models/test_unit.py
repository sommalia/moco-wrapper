import pytest

from moco_wrapper.util.response import JsonResponse, ListingResponse

from .. import IntegrationTest

class TestUnit(IntegrationTest):

    def test_get_list(self):
        with self.recorder.use_cassette("TestUnit.test_get_list"):
            response = self.moco.Unit.getlist()
            assert isinstance(response, ListingResponse)