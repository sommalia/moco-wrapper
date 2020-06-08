import pytest
from .. import UnitTest


class TestPurchaseCategory(UnitTest):
    def test_get(self):
        response = self.moco.PurchaseCategory.get(1)

        assert response["method"] == "GET"

    def test_getlist(self):
        response = self.moco.PurchaseCategory.getlist()

        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        sort_by = "testfield to sort by"

        response = self.moco.PurchaseCategory.getlist(sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "testfield to sort by"
        sort_order = "desc"

        response = self.moco.PurchaseCategory.getlist(sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        page_default = 1

        response = self.moco.PurchaseCategory.getlist()

        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.PurchaseCategory.getlist(page=page_overwrite)

        assert response["params"]["page"] == page_overwrite
