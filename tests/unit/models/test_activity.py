import pytest
from .. import UnitTest

class TestActivity(UnitTest):
    def test_create(self):
        date = "2019-10-10"
        project_id = 1
        task_id = 2
        hours = 4.5

        response = self.moco.Activity.create(, project_id , task_id, hours)
        response_data = response["data"] 
        assert response_data["date"] == date
        assert response_data["project_id"] == project_id
        assert response_data["task_id"] == task_id
        assert response_data["hours"] == hours