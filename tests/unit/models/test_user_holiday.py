from .. import UnitTest
import pytest

class TestUserHoliday(UnitTest):
    def test_getlist(self):
        year = 2019
        user_id = 4

        response = self.moco.UserHoliday.getlist(year=year, user_id=user_id)
        params = response["params"]

        assert params["year"] == year
        assert params["user_id"] == user_id
        assert response["method"] == "GET"


    def test_getlist_sort_default(self):
        sort_by = "field to sort by"

        response = self.moco.UserHoliday.getlist(sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "field to sort by"
        sort_order = "desc"

        response = self.moco.UserHoliday.getlist(sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        page_default = 1

        response = self.moco.UserHoliday.getlist()
        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.UserHoliday.getlist(page=page_overwrite)
        assert response["params"]["page"] == page_overwrite

    def test_get(self):
        holiday_id = 3

        response = self.moco.UserHoliday.get(holiday_id)

        assert response["method"] == "GET"


    def test_create(self):
        year = 2019
        title = "my vacation time"
        hours = 45
        user_id = 2

        response = self.moco.UserHoliday.create(year, title, hours=hours, user_id=user_id)
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

        response = self.moco.UserHoliday.update(holiday_id, year=year, title=title, hours=hours, user_id=user_id)
        data = response["data"]

        assert data["year"] == year
        assert data["title"] == title
        assert data["hours"] == hours
        assert data["user_id"] == user_id

        assert response["method"] == "PUT"

    def test_delete(self):
        holiday_id = 444

        response = self.moco.UserHoliday.delete(holiday_id)

        assert response["method"] == "DELETE"


    def test_create_with_days(self):
        year = 2019
        title = "my vacation time"
        days = 3
        user_id = 2

        response = self.moco.UserHoliday.create(year, title, days=days, user_id=user_id)
        data = response["data"]

        assert data["year"] == year
        assert data["title"] == title
        assert data["days"] == days
        assert data["user_id"] == user_id

        assert response["method"] == "POST"

    def test_create_throws_if_hours_none_days_none(self):
        with pytest.raises(ValueError):
            self.moco.UserHoliday.create(2019, "test title", hours=None, days=None, user_id=1)

    def test_create_throws_if_hours_set_days_set(self):
        with pytest.raises(ValueError):
            self.moco.UserHoliday.create(2019, "test title", hours=1, days=1, user_id=1)

    def test_update_with_days(self):
        holiday_id = 444
        year = 2019
        title = "my vacation time"
        days = 3
        user_id = 2

        response = self.moco.UserHoliday.update(holiday_id, year=year, title=title, days=days, user_id=user_id)
        data = response["data"]

        assert data["year"] == year
        assert data["title"] == title
        assert data["days"] == days
        assert data["user_id"] == user_id

        assert response["method"] == "PUT"

    def test_update_throws_if_hours_none_days_none(self):
        with pytest.raises(ValueError):
            self.moco.UserHoliday.update(1, days=None, hours=None)

    def test_update_throws_if_hours_set_days_set(self):
        with pytest.raises(ValueError):
            self.moco.UserHoliday.update(1, days=1, hours=1)