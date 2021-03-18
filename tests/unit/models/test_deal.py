import pytest

from .. import UnitTest


class TestDeal(UnitTest):
    def test_create(self):
        name = "deal name"
        currency = "EUR"
        money = 23143
        reminder_date = "2019-10-10"
        user_id = 25
        deal_category_id = 2
        company_id = 2
        info = "more deal information"
        status = "potential"
        closed_on = "2021-01-01"

        response = self.moco.Deal.create(
            name=name,
            currency=currency,
            money=money,
            reminder_date=reminder_date,
            user_id=user_id,
            deal_category_id=deal_category_id,
            company_id=company_id,
            info=info,
            status=status,
            closed_on=closed_on
        )

        data = response["data"]

        assert data["name"] == name
        assert data["currency"] == currency
        assert data["money"] == money
        assert data["reminder_date"] == reminder_date
        assert data["user_id"] == user_id
        assert data["deal_category_id"] == deal_category_id
        assert data["company_id"] == company_id
        assert data["info"] == info
        assert data["status"] == status
        assert data["closed_on"] == closed_on

        assert response["method"] == "POST"

    def test_create_default_status(self):
        name = "deal name"
        currency = "EUR"
        money = 23143
        reminder_date = "2019-10-10"
        user_id = 25
        deal_category_id = 2

        response = self.moco.Deal.create(
            name=name,
            currency=currency,
            money=money,
            reminder_date=reminder_date,
            user_id=user_id,
            deal_category_id=deal_category_id
        )

        data = response["data"]

        assert data["name"] == name
        assert data["currency"] == currency
        assert data["money"] == money
        assert data["reminder_date"] == reminder_date
        assert data["user_id"] == user_id
        assert data["deal_category_id"] == deal_category_id
        assert data["status"] == "pending"

    def test_update(self):
        deal_id = 333
        name = "deal name"
        currency = "EUR"
        money = 23143
        reminder_date = "2019-10-10"
        user_id = 25
        deal_category_id = 2
        company_id = 2
        info = "more deal information"
        status = "potential"
        closed_on = "2022-02-02"

        response = self.moco.Deal.update(
            deal_id=deal_id,
            name=name,
            currency=currency,
            money=money,
            reminder_date=reminder_date,
            user_id=user_id,
            deal_category_id=deal_category_id,
            company_id=company_id,
            info=info,
            status=status,
            closed_on=closed_on
        )

        data = response["data"]

        assert data["name"] == name
        assert data["currency"] == currency
        assert data["money"] == money
        assert data["reminder_date"] == reminder_date
        assert data["user_id"] == user_id
        assert data["deal_category_id"] == deal_category_id
        assert data["company_id"] == company_id
        assert data["info"] == info
        assert data["status"] == status
        assert data["closed_on"] == closed_on

        assert response["method"] == "PUT"

    def test_get(self):
        deal_id = 333

        response = self.moco.Deal.get(
            deal_id=deal_id
        )

        assert response["method"] == "GET"

    def test_getlist(self):
        status = "lost"
        tags = ["these", "are", "some", "test", "tags"]

        response = self.moco.Deal.getlist(
            status=status,
            tags=tags
        )

        params = response["params"]

        assert params["status"] == status
        assert params["tags"] == tags
        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        sort_by = "test field to sort by"

        response = self.moco.Deal.getlist(
            sort_by=sort_by
        )

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "test field to sort by"
        sort_order = "desc"

        response = self.moco.Deal.getlist(
            sort_by=sort_by,
            sort_order=sort_order
        )

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        page_default = 1

        response = self.moco.Deal.getlist()

        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.Deal.getlist(
            page=page_overwrite
        )

        assert response["params"]["page"] == page_overwrite
