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
            
            assert deal_create.response.status_code == 200

            assert isinstance(deal_create, JsonResponse)

            assert deal_create.data.name == "test deal create"
            assert deal_create.data.status == DealStatus.POTENTIAL
            assert deal_create.data.reminder_date == date(2020, 5, 1).isoformat()

    def test_get(self):
        with self.recorder.use_cassette("TestDeal.test_get"):
            user_id = self.moco.User.getlist().items[0].id
            deal_category_id = self.moco.DealCategory.getlist().items[0].id

            reminder_date = date(2020, 1, 10)
            money = 210

            deal_create = self.moco.Deal.create("test deal to get", "EUR", money, reminder_date, user_id, deal_category_id, status=DealStatus.WON)

            deal_get = self.moco.Deal.get(deal_create.data.id)

            assert deal_create.response.status_code == 200
            assert deal_get.response.status_code == 200

            assert isinstance(deal_create, JsonResponse)
            assert isinstance(deal_get, JsonResponse)

            assert deal_get.data.user.id == user_id
            assert deal_get.data.currency == "EUR"
            assert deal_get.data.reminder_date == reminder_date.isoformat()
            assert deal_get.data.money == money

    def test_getlist(self):
        with self.recorder.use_cassette("TestDeal.test_getlist"):
            deal_getlist = self.moco.Deal.getlist()

            assert deal_getlist.response.status_code == 200

            assert isinstance(deal_getlist, ListingResponse)

    def test_update(self):
        with self.recorder.use_cassette("TestDeal.test_update"):
            user_id = self.moco.User.getlist().items[0].id
            deal_category_id = self.moco.DealCategory.getlist().items[0].id

            reminder_date = date(2020, 1, 10)
            money = 210

            deal_create = self.moco.Deal.create("test deal to update", "EUR", money, reminder_date, user_id, deal_category_id, status=DealStatus.WON)

            update_reminder_date = date(2020, 5, 20)
            update_status = DealStatus.LOST
            update_money = 500
            update_name = "updated test deal"

            deal_update = self.moco.Deal.update(deal_create.data.id, name=update_name, money=update_money, reminder_date=update_reminder_date, status=update_status )

            assert deal_create.response.status_code == 200
            assert deal_update.response.status_code == 200

            assert isinstance(deal_create, JsonResponse)
            assert isinstance(deal_update, JsonResponse)

            assert deal_update.data.name == update_name
            assert deal_update.data.money == update_money
            assert deal_update.data.reminder_date == update_reminder_date.isoformat()
            assert deal_update.data.status == update_status