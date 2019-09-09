import pytest
from .. import UnitTest

class TestActivity(UnitTest):
    def test_create(self):
        date = "2019-10-10"
        project_id = 1
        task_id = 2
        hours = 4.5

        response = self.moco.Activity.create(date, project_id , task_id, hours)
        response_data = response["data"] 
        assert response_data["date"] == date
        assert response_data["project_id"] == project_id
        assert response_data["task_id"] == task_id
        assert response_data["hours"] == hours

        assert response["method"] == "POST"

    def test_getlist(self):
        from_date = "2019-01-01"
        to_date = "2020-01-01"
        user_id = 21
        project_id = 22

        response = self.moco.Activity.getlist(from_date=from_date, to_date=to_date, user_id=user_id, project_id=project_id)

        response_params = response["params"]
        assert response_params["from"] == from_date
        assert response_params["to"] == to_date
        assert response_params["user_id"] == user_id
        assert response_params["project_id"] == project_id

        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        sort_by = "sort by field"
        response = self.moco.Activity.getlist(sort_by=sort_by)

        response_params = response["params"]
        assert response_params["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "sort by field"
        sort_order = "desc"
        response = self.moco.Activity.getlist(sort_by=sort_by, sort_order=sort_order)

        response_params = response["params"]
        assert response_params["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_get(self):
        activity_id = 21
        response = self.moco.Activity.get(activity_id)

        assert response["params"] == None
        assert response["data"] == None
        assert response["method"] == "GET"

    def test_update(self):
        project_id = 12412
        task_id = 22
        hours = 4.5
        activity_id = 33

        response = self.moco.Activity.update(activity_id, project_id=project_id, task_id=task_id, hours=hours)
        response_data = response["data"]

        assert response_data["project_id"] == project_id
        assert response_data["task_id"] == task_id
        assert response_data["hours"] == hours

        assert response["method"] == "PUT"

    def test_start_timer(self):
        activity_id = 123

        response = self.moco.Activity.start_timer(activity_id)
        
        assert response["method"] == "PATCH"

    def test_stop_timer(self):
        activity_id = 123

        response = self.moco.Activity.stop_timer(activity_id)

        assert response["method"] == "PATCH"

    def test_delete(self):
        activity_id = 123

        response = self.moco.Activity.delete(activity_id)

        assert response["method"] == "DELETE"

    def test_disregard(self):
        reason = "because i said so"
        activity_ids = [123, 124, 125]
        project_id = 1
        customer_id = 2

        response = self.moco.Activity.disregard(reason, activity_ids, customer_id, project_id)
        response_data = response["data"]

        assert response_data["reason"] == reason
        assert response_data["activity_ids"] == activity_ids
        assert response_data["project_id"] == project_id
        assert response_data["customer_id"] == customer_id   

        assert response["method"] == "POST"     
