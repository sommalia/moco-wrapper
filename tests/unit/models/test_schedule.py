import pytest

from .. import UnitTest


class TestSchedule(UnitTest):
    def test_getlist(self):
        from_date = '2019-10-10'
        to_date = '2015-05-05'
        user_id = 4
        absence_code = 342

        response = self.moco.Schedule.getlist(
            from_date=from_date,
            to_date=to_date,
            user_id=user_id,
            absence_code=absence_code
        )
        params = response["params"]

        assert params["from"] == from_date
        assert params["to"] == to_date
        assert params["user_id"] == user_id
        assert params["absence_code "] == absence_code

        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        sort_by = "testfield to sort by"

        response = self.moco.Schedule.getlist(sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "testfield to sort by"
        sort_order = "desc"

        response = self.moco.Schedule.getlist(sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        page_default = 1

        response = self.moco.Schedule.getlist()
        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.Schedule.getlist(page=page_overwrite)
        assert response["params"]["page"] == page_overwrite

    def test_get(self):
        schedule_id = 1234

        response = self.moco.Schedule.get(schedule_id)

        assert response["method"] == "GET"

    def test_create(self):
        date = "2019-10-10"
        absence_code = 5
        user_id = 234
        am = True
        pm = True
        comment = "this is the comment comment"
        overwrite = True

        response = self.moco.Schedule.create(
            schedule_date=date,
            absence_code=absence_code,
            user_id=user_id,
            am=am,
            pm=pm,
            comment=comment,
            overwrite=overwrite
        )
        data = response["data"]

        assert data["date"] == date
        assert data["absence_code"] == absence_code
        assert data["user_id"] == user_id
        assert data["am"] == am
        assert data["pm"] == pm
        assert data["comment"] == comment
        assert data["overwrite"] == overwrite

        assert response["method"] == "POST"

    def test_update(self):
        schedule_id = 2434
        absence_code = 5
        am = True
        pm = True
        comment = "this is the comment comment"
        overwrite = True

        response = self.moco.Schedule.update(
            schedule_id=schedule_id,
            absence_code=absence_code,
            am=am,
            pm=pm,
            comment=comment,
            overwrite=overwrite
        )
        data = response["data"]

        assert data["absence_code"] == absence_code
        assert data["am"] == am
        assert data["pm"] == pm
        assert data["comment"] == comment
        assert data["overwrite"] == overwrite

        assert response["method"] == "PUT"


    def test_delete(self):
        schedule_id = 2354

        response = self.moco.Schedule.delete(schedule_id)

        assert response["method"] == "DELETE"
