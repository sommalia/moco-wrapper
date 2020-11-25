from .. import IntegrationTest
from moco_wrapper.util.response import ListResponse


class TestPurchaseCategory(IntegrationTest):

    def test_getlist(self):
        with self.recorder.use_cassette("TestPurchaseCategory.test_getlist"):
            category_list = self.moco.PurchaseCategory.getlist()

            assert category_list.response.status_code == 200

            assert type(category_list) is ListResponse

