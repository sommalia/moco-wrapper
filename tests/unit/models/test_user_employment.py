from .. import UnitTest


class TestUserEmployment(UnitTest):
    """class for testing the employment model"""

    def test_getlist(self):
        from_date = "2019-10-10"
        to_date = "2020-10-10"
        user_id = 2

        response = self.moco.UserEmployment.getlist(
            from_date=from_date,
            to_date=to_date,
            user_id=user_id
        )

        params = response["params"]

        assert params["from"] == from_date
        assert params["to"] == to_date
        assert params["user_id"] == user_id
        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        sort_by = "this is the field to sort by"

        response = self.moco.UserEmployment.getlist(
            sort_by=sort_by
        )

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "this is the field to sort by"
        sort_order = "desc"

        response = self.moco.UserEmployment.getlist(
            sort_by=sort_by,
            sort_order=sort_order
        )

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        page_default = 1

        response = self.moco.UserEmployment.getlist()

        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.UserEmployment.getlist(
            page=page_overwrite
        )

        assert response["params"]["page"] == page_overwrite

    def test_get(self):
        employment_id = 44

        response = self.moco.UserEmployment.get(
            employment_id=employment_id
        )

        assert response["method"] == "GET"
