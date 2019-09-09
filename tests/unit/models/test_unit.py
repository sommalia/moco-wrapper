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