from moco_wrapper.util.response import JsonResponse, ListingResponse
from moco_wrapper.models.deal import DealStatus

from datetime import date

from .. import IntegrationTest

class TestDeal(IntegrationTest):
    def test_create(self):
        with self.recorder.use_cassette("TestDeal.test_create"):
        user_id = self.moco.User.getlist().items[0].id
        deal_category_id = self.moco.DealCategory.getlist().items[0].id

        deal_create = self.moco.Deal.create("test deal create", "EUR", 200.05, date(2020, 5, 1), user_id, deal_category_id, status=DealStatus.POTENTIAL)
        print(deal_create)

        assert deal_create.response.status_code == 200

        assert 