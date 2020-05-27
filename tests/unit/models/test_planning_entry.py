from .. import UnitTest
import pytest


class TestPlanningEntry(UnitTest):
    def test_getlist(self):
        start_date = '2019-10-10'
        end_date = '2020-10-10'
        user_id = 1
        project_id = 2

        response = self.moco.PlanningEntry.getlist(
            start_date=start_date,
            end_date=end_date,
            user_id=user_id,
            project_id=project_id
        )
        params = response["params"]

        assert params["period"] == "{}:{}".format(start_date, end_date)
        assert params["user_id"] == user_id
        assert params["project_id"] == project_id

        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        sort_by = "field to sort by"

        response = self.moco.PlanningEntry.getlist(sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "field to sort by"
        sort_order = "desc"

        response = self.moco.PlanningEntry.getlist(sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        page_default = 1

        response = self.moco.PlanningEntry.getlist()
        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.PlanningEntry.getlist(page=page_overwrite)
        assert response["params"]["page"] == page_overwrite

    def test_getlist_throws_only_start_date(self):
        with pytest.raises(ValueError):
            response = self.moco.PlanningEntry.getlist(start_date='2020-02-10', end_date=None)

    def test_getlist_throws_only_end_date(self):
        with pytest.raises(ValueError):
            response = self.moco.PlanningEntry.getlist(start_date=None, end_date='2020-10-10')

    def test_get(self):
        entry_id = 12345

        response = self.moco.PlanningEntry.get(entry_id)

        assert response["method"] == "GET"

    def test_create(self):
        project_id = 1234
        starts_on = "2020-02-12"
        ends_on = "2020-10-10"
        hours_per_day = 3.5
        user_id = 1
        comment = "This is the comment"
        symbol = 2

        response = self.moco.PlanningEntry.create(
            project_id,
            starts_on,
            ends_on,
            hours_per_day,
            user_id=user_id,
            comment=comment,
            symbol=symbol
        )
        data = response["data"]

        assert data["project_id"] == project_id
        assert data["starts_on"] == starts_on
        assert data["ends_on"] == ends_on
        assert data["hours_per_day"] == hours_per_day
        assert data["user_id"] == user_id
        assert data["comment"] == comment
        assert data["symbol"] == symbol

        assert response["method"] == "POST"

    def test_update(self):
        entry_id = 3554
        project_id = 1234
        starts_on = "2020-02-12"
        ends_on = "2020-10-10"
        hours_per_day = 3.5
        user_id = 1
        comment = "This is the comment"
        symbol = 2

        response = self.moco.PlanningEntry.update(
            entry_id,
            project_id=project_id,
            starts_on=starts_on,
            ends_on=ends_on,
            hours_per_day=hours_per_day,
            user_id=user_id,
            comment=comment,
            symbol=symbol
        )
        data = response["data"]

        assert data["project_id"] == project_id
        assert data["starts_on"] == starts_on
        assert data["ends_on"] == ends_on
        assert data["hours_per_day"] == hours_per_day
        assert data["user_id"] == user_id
        assert data["comment"] == comment
        assert data["symbol"] == symbol

        assert response["method"] == "PUT"
