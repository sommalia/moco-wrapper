from moco_wrapper.util.response import JsonResponse, ListingResponse
from moco_wrapper.models.deal import DealStatus

from datetime import date

from .. import IntegrationTest

class TestDeal(IntegrationTest):
    def get_user(self):
        with self.recorder.use_cassette("TestDeal.get_user"):
            user = self.moco.User.getlist().items[0]
            return user

    def get_deal_category(self):
        with self.recorder.use_cassette("TestDeal.get_deal_category"):
            cat = self.moco.DealCategory.getlist().items[0]
            return cat

    def get_company(self):
        with self.recorder.use_cassette("TestDeal.get_company"):
            company_create = self.moco.Company.create(
                "TestDeal",
                company_type="customer"
            )

            return company_create.data


    def test_create(self):
        user = self.get_user()
        category = self.get_deal_category()

        with self.recorder.use_cassette("TestDeal.test_create"):
            name = "deal create test"
            currency = "EUR"
            money = 200
            reminder_date = date(2020, 1, 1)
            status = DealStatus.PENDING

            deal_create = self.moco.Deal.create(
                name,
                currency,
                money,
                reminder_date,
                user.id,
                category.id,
                status=status
            )
            
            assert deal_create.response.status_code == 200

            assert isinstance(deal_create, JsonResponse)

            assert deal_create.data.name == name
            assert deal_create.data.currency == currency
            assert deal_create.data.money == money
            assert deal_create.data.reminder_date == reminder_date.isoformat()
            assert deal_create.data.user.id == user.id
            assert deal_create.data.category.id == category.id
            assert deal_create.data.status == status

    def test_create_full(self):
        user = self.get_user()
        category = self.get_deal_category()
        company = self.get_company()

        with self.recorder.use_cassette("TestDeal.test_create_full"):
            name = "deal create test"
            currency = "EUR"
            money = 200
            reminder_date = date(2020, 1, 1)
            status = DealStatus.PENDING
            info = "more info"


            deal_create = self.moco.Deal.create(
                name,
                currency,
                money,
                reminder_date,
                user.id,
                category.id,
                status=status,
                company_id=company.id,
                info=info,
            )
            
            assert deal_create.response.status_code == 200

            assert isinstance(deal_create, JsonResponse)

            assert deal_create.data.name == name
            assert deal_create.data.currency == currency
            assert deal_create.data.money == money
            assert deal_create.data.reminder_date == reminder_date.isoformat()
            assert deal_create.data.user.id == user.id
            assert deal_create.data.category.id == category.id
            assert deal_create.data.status == status
            assert deal_create.data.company.id == company.id
            assert deal_create.data.info == info

    def test_get(self):
        user = self.get_user()
        category = self.get_deal_category()

        with self.recorder.use_cassette("TestDeal.test_get"):
            name = "test deal to get"
            currency = "EUR"
            reminder_date = date(2020, 1, 10)
            money = 210
            status = DealStatus.WON

            deal_create = self.moco.Deal.create(
                name,
                currency, 
                money, 
                reminder_date, 
                user.id, 
                category.id, 
                status=status
            )

            deal_get = self.moco.Deal.get(deal_create.data.id)

            assert deal_create.response.status_code == 200
            assert deal_get.response.status_code == 200

            assert isinstance(deal_create, JsonResponse)
            assert isinstance(deal_get, JsonResponse)

            assert deal_get.data.name == name
            assert deal_get.data.currency == currency
            assert deal_get.data.reminder_date == reminder_date.isoformat()
            assert deal_get.data.money == money
            assert deal_get.data.user.id == user.id
            assert deal_get.data.category.id == category.id
            assert deal_get.data.status == status

    def test_getlist(self):
        with self.recorder.use_cassette("TestDeal.test_getlist"):
            deal_getlist = self.moco.Deal.getlist()

            assert deal_getlist.response.status_code == 200

            assert isinstance(deal_getlist, ListingResponse)

            assert deal_getlist.current_page == 1
            assert deal_getlist.is_last is not None
            assert deal_getlist.next_page is not None
            assert deal_getlist.total is not None
            assert deal_getlist.page_size is not None

    def test_update(self):
        user = self.get_user()
        category = self.get_deal_category()
        company = self.get_company()

        with self.recorder.use_cassette("TestDeal.test_update"):
            deal_create = self.moco.Deal.create(
                "dummy deal, test update",
                "EUR",
                0,
                date(2000, 1, 1),
                user.id,
                category.id
            )

            name = "updated deal"
            currency = "EUR"
            money = 400
            reminder_date = date(2020, 1, 1)
            info = "updated info"
            status = DealStatus.POTENTIAL

            deal_update = self.moco.Deal.update(
                deal_create.data.id, 
                name=name,
                currency=currency,
                money=money,
                reminder_date=reminder_date,
                user_id=user.id,
                deal_category_id=category.id,
                company_id=company.id,
                info=info,
                status=status
            )

            assert deal_create.response.status_code == 200
            assert deal_update.response.status_code == 200

            assert isinstance(deal_create, JsonResponse)
            assert isinstance(deal_update, JsonResponse)

            assert deal_update.data.name == name
            assert deal_update.data.currency == currency
            assert deal_update.data.money == money
            assert deal_update.data.reminder_date == reminder_date.isoformat()
            assert deal_update.data.user.id == user.id
            assert deal_update.data.category.id == category.id
            assert deal_update.data.company.id == company.id
            assert deal_update.data.info == info
            assert deal_update.data.status == status
            