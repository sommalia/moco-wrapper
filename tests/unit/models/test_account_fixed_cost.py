import pytest
from .. import UnitTest


class TestAccountFixedCost(UnitTest):

    def test_getlist(self):
        year = 2020

        response = self.moco.AccountFixedCost.getlist(
            year=year
        )

        params = response["params"]

        assert params["year"] == year

        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        sort_by = "sort by field"

        response = self.moco.AccountFixedCost.getlist(
            sort_by=sort_by
        )

        params = response["params"]

        assert params["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "sort by field"
        sort_order = "desc"

        response = self.moco.AccountFixedCost.getlist(
            sort_by=sort_by,
            sort_order=sort_order
        )

        params = response["params"]

        assert params["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        default_page = 1

        response = self.moco.AccountFixedCost.getlist()

        params = response["params"]

        assert params["page"] == default_page

    def test_getlist_page_overwrite(self):
        overwrite_page = 2

        response = self.moco.AccountFixedCost.getlist(
            page=overwrite_page
        )

        params = response["params"]

        assert params["page"] == overwrite_page

