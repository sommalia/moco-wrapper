from moco_wrapper.util.response import ObjectResponse, PagedListResponse
from moco_wrapper.models.deal import DealStatus
from moco_wrapper.models.company import CompanyType

from datetime import date

from .. import IntegrationTest


class TestDeal(IntegrationTest):
    def get_user(self):
        with self.recorder.use_cassette("TestDeal.get_user"):
            user = self.moco.User.getlist()[0]
            return user

    def get_deal_category(self):
        with self.recorder.use_cassette("TestDeal.get_deal_category"):
            cat = self.moco.DealCategory.getlist()[0]
            return cat

    def get_company(self):
        with self.recorder.use_cassette("TestDeal.get_company"):
            company_create = self.moco.Company.create(
                name="TestDeal.get_company",
                company_type=CompanyType.CUSTOMER
            )

            return company_create.data

    def test_create(self):
        user = self.get_user()
        category = self.get_deal_category()

        with self.recorder.use_cassette("TestDeal.test_create"):
            name = "TestDeal.test_create"
            currency = "EUR"
            money = 200
            reminder_date = date(2020, 1, 1)
            status = DealStatus.PENDING

            deal_create = self.moco.Deal.create(
                name=name,
                currency=currency,
                money=money,
                reminder_date=reminder_date,
                user_id=user.id,
                deal_category_id=category.id,
                status=status
            )

            assert deal_create.response.status_code == 200

            assert type(deal_create) is ObjectResponse

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
            name = "TestDeal.test_create_full"
            currency = "EUR"
            money = 200
            reminder_date = date(2020, 1, 1)
            status = DealStatus.LOST
            info = "more info"
            closed_on = date(2021, 1, 1)
            tags = ["test", "create", "deal", "tags"]

            deal_create = self.moco.Deal.create(
                name=name,
                currency=currency,
                money=money,
                reminder_date=reminder_date,
                user_id=user.id,
                deal_category_id=category.id,
                status=status,
                company_id=company.id,
                info=info,
                closed_on=closed_on,
                tags=tags
            )

            assert deal_create.response.status_code == 200

            assert type(deal_create) is ObjectResponse

            assert deal_create.data.name == name
            assert deal_create.data.currency == currency
            assert deal_create.data.money == money
            assert deal_create.data.reminder_date == reminder_date.isoformat()
            assert deal_create.data.user.id == user.id
            assert deal_create.data.category.id == category.id
            assert deal_create.data.status == status
            assert deal_create.data.company.id == company.id
            assert deal_create.data.info == info
            assert deal_create.data.closed_on == closed_on.isoformat()
            assert deal_create.data.tags == sorted(tags)

    def test_get(self):
        user = self.get_user()
        category = self.get_deal_category()

        with self.recorder.use_cassette("TestDeal.test_get"):
            name = "TestDeal.test_get_create"
            currency = "EUR"
            reminder_date = date(2020, 1, 10)
            money = 210
            status = DealStatus.WON

            deal_create = self.moco.Deal.create(
                name=name,
                currency=currency,
                money=money,
                reminder_date=reminder_date,
                user_id=user.id,
                deal_category_id=category.id,
                status=status
            )

            deal_get = self.moco.Deal.get(
                deal_id=deal_create.data.id
            )

            assert deal_create.response.status_code == 200
            assert deal_get.response.status_code == 200

            assert type(deal_create) is ObjectResponse
            assert type(deal_get) is ObjectResponse

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

            assert type(deal_getlist) is PagedListResponse

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
                name="TestDeal.test_update_create",
                currency="EUR",
                money=0,
                reminder_date=date(2000, 1, 1),
                user_id=user.id,
                deal_category_id=category.id
            )

            name = "TestDeal.test_update"
            currency = "EUR"
            money = 400
            reminder_date = date(2020, 1, 1)
            info = "updated info"
            status = DealStatus.DROPPED
            closed_on = date(2021, 1, 1)
            tags = ["these", "update", "other"]

            deal_update = self.moco.Deal.update(
                deal_id=deal_create.data.id,
                name=name,
                currency=currency,
                money=money,
                reminder_date=reminder_date,
                user_id=user.id,
                deal_category_id=category.id,
                company_id=company.id,
                info=info,
                status=status,
                closed_on=closed_on,
                tags=tags
            )

            assert deal_create.response.status_code == 200
            assert deal_update.response.status_code == 200

            assert type(deal_create) is ObjectResponse
            assert type(deal_update) is ObjectResponse

            assert deal_update.data.name == name
            assert deal_update.data.currency == currency
            assert deal_update.data.money == money
            assert deal_update.data.reminder_date == reminder_date.isoformat()
            assert deal_update.data.user.id == user.id
            assert deal_update.data.category.id == category.id
            assert deal_update.data.company.id == company.id
            assert deal_update.data.info == info
            assert deal_update.data.status == status
            assert deal_update.data.closed_on == closed_on.isoformat()
            assert deal_update.data.tags == sorted(tags)

    def test_closed_on_not_set_when_pending(self):
        user = self.get_user()
        category = self.get_deal_category()

        with self.recorder.use_cassette("TestDeal.test_closed_on_not_set_when_pending"):
            name = "TestDeal.test_create"
            currency = "EUR"
            money = 200
            reminder_date = date(2020, 1, 1)
            status = DealStatus.PENDING
            closed_on = date(2021, 1, 1)

            deal_create = self.moco.Deal.create(
                name=name,
                currency=currency,
                money=money,
                reminder_date=reminder_date,
                user_id=user.id,
                deal_category_id=category.id,
                status=status,
                closed_on=closed_on
            )

            assert deal_create.response.status_code == 200

            assert deal_create.data.closed_on == ''

