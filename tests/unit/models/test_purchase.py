import pytest
from .. import UnitTest


class TestPurchase(UnitTest):
    def test_getlist_sort_default(self):
        sort_by = "field to sort by"

        response = self.moco.Purchase.getlist(sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "field to sort by"
        sort_order = "desc"

        response = self.moco.Purchase.getlist(sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        page_default = 1

        response = self.moco.Purchase.getlist()
        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.Purchase.getlist(page=page_overwrite)
        assert response["params"]["page"] == page_overwrite

    def test_getlist_throws_only_start_date(self):
        with pytest.raises(ValueError):
            response = self.moco.Purchase.getlist(start_date='2020-02-10', end_date=None)

    def test_getlist_throws_only_end_date(self):
        with pytest.raises(ValueError):
            response = self.moco.Purchase.getlist(start_date=None, end_date='2020-10-10')

    def test_getlist(self):
        purchase_id = 123
        category_id = 456
        term = "this is the term"
        company_id = 444
        status = "pending"
        tags = ["these", "are", "tags"]
        start_date = "2020-01-04"
        end_date = "2020-04-04"
        unpaid = True

        response = self.moco.Purchase.getlist(
            purchase_id=purchase_id,
            category_id=category_id,
            term=term,
            company_id=company_id,
            status=status,
            tags=tags,
            start_date=start_date,
            end_date=end_date,
            unpaid=unpaid
        )
        params = response["params"]

        assert response["method"] == "GET"

        assert params["id"] == purchase_id
        assert params["category_id"] == category_id
        assert params["term"] == term
        assert params["company_id"] == company_id
        assert params["status"] == status
        assert sorted(params["tags"]) == sorted(tags)
        assert params["date"] == "{}:{}".format(start_date, end_date)
        assert params["unpaid"] == unpaid
