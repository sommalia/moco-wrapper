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

    def test_getlist_sort_default(self):
        sort_by = "test field to sort by"

        response = self.moco.DealCategory.getlist(sort_by=sort_by)
        
        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "test field to sort by"
        sort_order = "desc"

        response = self.moco.DealCategory.getlist(sort_by=sort_by, sort_order=sort_order)
        
        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)   

    def test_getlist_page_default(self):
        page_default = 1

        response = self.moco.DealCategory.getlist()
        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.DealCategory.getlist(page=page_overwrite)
        assert response["params"]["page"] == page_overwrite
