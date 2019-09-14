from .. import UnitTest

class TestEmployment(UnitTest):
    """class for testing the employment model"""
    
    def test_getlist(self):
        from_date = "2019-10-10"
        to_date = "2020-10-10"
        user_id = 2

        response = self.moco.Employment.getlist(from_date=from_date, to_date=to_date, user_id=user_id)
        params = response["params"]

        assert params["from"] == from_date
        assert params["to"] == to_date
        assert params["user_id"] == user_id
        assert response["method"] == "GET"


    def test_getlist_sort_default(self):
        sort_by = "this is the field to sort by"

        response = self.moco.Employment.getlist(sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "this is the field to sort by"
        sort_order = "desc"

        response = self.moco.Employment.getlist(sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_get(self):
        employement_id = 44

        response = self.moco.Employment.get(employement_id)

        assert response["method"] == "GET"