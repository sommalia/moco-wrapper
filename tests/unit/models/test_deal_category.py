import pytest

from .. import UnitTest

class TestDealCategory(UnitTest):

    def test_create(self):
        name = "test deal category"
        prob = 15

        response = self.moco.DealCategory.create(name, prob)
        data = response["data"]

        assert data["name"] == name
        assert data["probability"] == prob

        assert response["method"] == "POST"

    def test_update(self):
        cat_id = 22
        name = "test deal category to update"
        prob = 32

        response = self.moco.DealCategory.update(cat_id, name, prob)
        data = response["data"]

        assert data["name"] == name
        assert data["probability"] == prob

        assert response["method"] == "PUT"

    def test_get(self):
        deal_id = 333

        response = self.moco.DealCategory.get(deal_id)

        assert response["method"] == "GET"

    def test_delete(self):
        cat_id = 22

        response = self.moco.DealCategory.delete(cat_id)

        assert response["method"] == "DELETE"





