from .. import UnitTest
import pytest


class TestPresence(UnitTest):

    def test_getlist(self):
        from_date = '2019-10-10'
        to_date = '2020-10-10'
        user_id = 4

        response = self.moco.Presence.getlist(from_date=from_date, to_date=to_date, user_id=user_id)
        params = response["params"]

        assert params["from"] == from_date
        assert params["to"] == to_date
        assert params["user_id"] == user_id
        assert response["method"] == "GET"


    def test_getlist_sort_default(self):
        sort_by = "test field to sort by"

        response = self.moco.Presence.getlist(sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "test field to sort by"
        sort_order = "desc"

        response = self.moco.Presence.getlist(sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        page_default = 1

        response = self.moco.Presence.getlist()
        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.Presence.getlist(page=page_overwrite)
        assert response["params"]["page"] == page_overwrite


    def test_get(self):
        presence_id = 123

        response = self.moco.Presence.get(presence_id)

        assert response["method"] == "GET"

    def test_create(self):
        date = '2019-10-10'
        from_time = '08:00'
        to_time = '14:00'

        response = self.moco.Presence.create(date, from_time, to_time=to_time)
        data = response["data"]

        assert data["date"] == date
        assert data["from"] == from_time
        assert data["to"] == to_time
        assert response["method"] == "POST"

    def test_touch(self):
        
        response = self.moco.Presence.touch()

        assert response["method"] == "POST"
    
    def test_update(self):
        presence_id = 123
        date = '2019-10-10'
        from_time = '08:00'
        to_time = '14:00'

        response = self.moco.Presence.update(presence_id, pres_date=date, to_time=to_time, from_time=from_time)
        data = response["data"]

        assert data["date"] == date
        assert data["from"] == from_time
        assert data["to"] == to_time
        assert response["method"] == "PUT"


    def test_delete(self):
        presence_id = 123

        response = self.moco.Presence.delete(presence_id)

        assert response["method"] == "DELETE"