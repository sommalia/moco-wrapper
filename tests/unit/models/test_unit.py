import pytest
from .. import UnitTest

class TestUnit(UnitTest):
    def test_get(self):
        unit_id = 25

        response = self.moco.Unit.get(unit_id)
        
        assert response["method"] == "GET"

    def test_getlist(self):
        response = self.moco.Unit.getlist()

        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        sort_by = "sort by field"

        response = self.moco.Unit.getlist(sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "sort by field"
        sort_order = "desc"

        response = self.moco.Unit.getlist(sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        page_default = 1

        response = self.moco.Unit.getlist()
        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.Unit.getlist(page=page_overwrite)
        assert response["params"]["page"] == page_overwrite
        