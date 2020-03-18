from .. import IntegrationTest
from moco_wrapper.util.response import ListingResponse

class TestPurchaseCategory(IntegrationTest):

    def test_getlist(self):
        with self.recorder.use_cassette("TestPurchaseCategory.test_getlist"):
            category_list = self.moco.PurchaseCategory.getlist()
        
            assert category_list.response.status_code == 200

            assert isinstance(category_list, ListingResponse)

            assert category_list.current_page == 1
            assert category_list.is_last is not None
            assert category_list.next_page is not None
            assert category_list.total is not None
            assert category_list.page_size is not None