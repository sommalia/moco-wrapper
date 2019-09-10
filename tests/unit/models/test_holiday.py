from .. import UnitTest
import pytest

class TestHoliday(UnitTest):
    def test_getlist(self):
        year = 2019
        user_id = 4

        response = self.moco.Holiday.getlist(year=year, user_id=user_id)
        params = response["params"]

        assert params["year"] == year
        assert params["user_id"] == user_id
        assert response["method"] == "GET"


    def test_getlist_sort_default(self):
        sort_by = "field to sort by"

        response = self.moco.Holiday.getlist(sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "field to sort by"
        sort_order = "desc"

        response = self.moco.Holiday.getlist(sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)


    def test_get(self):
        holiday_id = 3

        response = self.moco.Holiday.get(holiday_id)

        assert response["method"] == "GET"


    def test_create(self):
        year = 2019
        title = "my vacation time"
        hours = 45
        user_id = 2

        response = self.moco.Holiday.create(year, title, hours=hours, user_id=user_id)
        data = response["data"]

        assert data["year"] == year
        assert data["title"] == title
        assert data["hours"] == hours
        assert data["user_id"] == user_id

        assert response["method"] == "POST"

    def test_update(self):
        holiday_id = 444
        year = 2019
        title = "my vacation time"
        hours = 45
        user_id = 2

        response = self.moco.Holiday.update(holiday_id, year=year, title=title, hours=hours, user_id=user_id)
        data = response["data"]

        assert data["year"] == year
        assert data["title"] == title
        assert data["hours"] == hours
        assert data["user_id"] == user_id

        assert response["method"] == "PUT"

    def test_delete(self):
        holiday_id = 444

        response = self.moco.Holiday.delete(holiday_id)

        assert response["method"] == "DELETE"