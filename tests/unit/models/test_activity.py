import pytest
from .. import UnitTest


class TestActivity(UnitTest):
    def test_create(self):
        date = "2019-10-10"
        project_id = 1
        task_id = 2
        hours = 4.5

        response = self.moco.Activity.create(
            activity_date=date,
            project_id=project_id,
            task_id=task_id,
            hours=hours
        )

        data = response["data"]

        assert data["date"] == date
        assert data["project_id"] == project_id
        assert data["task_id"] == task_id
        assert data["hours"] == hours

        assert response["method"] == "POST"

    def test_getlist(self):
        from_date = "2019-01-01"
        to_date = "2020-01-01"
        user_id = 21
        project_id = 22
        task_id = 23

        response = self.moco.Activity.getlist(
            from_date=from_date,
            to_date=to_date,
            user_id=user_id,
            project_id=project_id,
            task_id=task_id
        )

        params = response["params"]

        assert params["from"] == from_date
        assert params["to"] == to_date
        assert params["user_id"] == user_id
        assert params["project_id"] == project_id
        assert params["task_id"] == task_id

        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        from_date = "2019-01-01"
        to_date = "2020-01-01"
        sort_by = "sort by field"

        response = self.moco.Activity.getlist(
            from_date=from_date,
            to_date=to_date,
            sort_by=sort_by
        )

        params = response["params"]

        assert params["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        from_date = "2019-01-01"
        to_date = "2020-01-01"
        sort_by = "sort by field"
        sort_order = "desc"

        response = self.moco.Activity.getlist(
            from_date=from_date,
            to_date=to_date,
            sort_by=sort_by,
            sort_order=sort_order
        )

        params = response["params"]

        assert params["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        from_date = "2019-01-01"
        to_date = "2020-01-01"
        default_page = 1

        response = self.moco.Activity.getlist(
            from_date=from_date,
            to_date=to_date
        )

        params = response["params"]

        assert params["page"] == default_page

    def test_getlist_page_overwrite(self):
        from_date = "2019-01-01"
        to_date = "2020-01-01"
        overwrite_page = 22

        response = self.moco.Activity.getlist(
            from_date=from_date,
            to_date=to_date,
            page=overwrite_page
        )

        params = response["params"]

        assert params["page"] == overwrite_page

    def test_get(self):
        activity_id = 21

        response = self.moco.Activity.get(activity_id=activity_id)

        assert response["method"] == "GET"

    def test_update(self):
        project_id = 12412
        task_id = 22
        hours = 4.5
        activity_id = 33

        response = self.moco.Activity.update(
            activity_id=activity_id,
            project_id=project_id,
            task_id=task_id,
            hours=hours
        )

        data = response["data"]

        assert data["project_id"] == project_id
        assert data["task_id"] == task_id
        assert data["hours"] == hours

        assert response["method"] == "PUT"

    def test_start_timer(self):
        activity_id = 123

        response = self.moco.Activity.start_timer(
            activity_id=activity_id
        )

        assert response["method"] == "PATCH"

    def test_stop_timer(self):
        activity_id = 123

        response = self.moco.Activity.stop_timer(
            activity_id=activity_id
        )

        assert response["method"] == "PATCH"

    def test_delete(self):
        activity_id = 123

        response = self.moco.Activity.delete(
            activity_id=activity_id
        )

        assert response["method"] == "DELETE"

    def test_disregard(self):
        reason = "because i said so"
        activity_ids = [123, 124, 125]
        project_id = 1
        company_id = 2

        response = self.moco.Activity.disregard(
            reason=reason,
            activity_ids=activity_ids,
            company_id=company_id,
            project_id=project_id
        )

        data = response["data"]

        assert data["reason"] == reason
        assert data["activity_ids"] == activity_ids
        assert data["project_id"] == project_id
        assert data["company_id"] == company_id

        assert response["method"] == "POST"

    def test_getlist_task_without_project_throws(self):
        from_date = "2019-01-01"
        to_date = "2020-01-01"
        task_id = 22

        with pytest.raises(ValueError) as e:
            response = self.moco.Activity.getlist(
                from_date=from_date,
                to_date=to_date,
                task_id=task_id
            )
