import pytest
from .. import UnitTest


class TestPurchaseCategory(UnitTest):
    def test_get(self):
        response = self.moco.PurchaseCategory.get(1)

        assert response["method"] == "GET"

    def test_getlist(self):
        response = self.moco.PurchaseCategory.getlist()

        assert response["method"] == "GET"


