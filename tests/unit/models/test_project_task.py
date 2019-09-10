from .. import UnitTest
import pytest

class TestProjectTask(UnitTest):
    def test_getlist(self):
        project_id = 2

        response = self.moco.ProjectTask.getlist(project_id)

        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        project_id = 2
        sort_by = "field to sort by"

        response = self.moco.ProjectTask.getlist(project_id, sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        project_id = 2
        sort_by = "field to sort by"
        sort_order = "desc"

        response = self.moco.ProjectTask.getlist(project_id, sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_get(self):
        project_id = 2
        task_id = 3

        response = self.moco.ProjectTask.get(project_id, task_id)

        assert response["method"] == "GET"

    def test_create(self):
        project_id = 2
        name = "my new task"
        billable = False
        active = True
        budget = 400
        hourly_rate = 20

        response = self.moco.ProjectTask.create(project_id, name, billable=billable, active=active, budget=budget, hourly_rate=hourly_rate)
        data = response["data"]

        assert data["name"] == name
        assert data["billable"] == billable
        assert data["active"] == active
        assert data["budget"] == budget
        assert data["hourly_rate"] == hourly_rate
        assert response["method"] == "POST"


    def test_update(self):
        project_id = 2
        task_id = 89
        name = "my new task"
        billable = False
        active = True
        budget = 400
        hourly_rate = 20

        response = self.moco.ProjectTask.update(project_id, task_id, name=name, billable=billable, active=active, budget=budget, hourly_rate=hourly_rate)
        data = response["data"]

        assert data["name"] == name
        assert data["billable"] == billable
        assert data["active"] == active
        assert data["budget"] == budget
        assert data["hourly_rate"] == hourly_rate
        assert response["method"] == "PUT"

    def test_delete(self):
        project_id = 2
        task_id = 3

        response = self.moco.ProjectTask.delete(project_id, task_id)

        assert response["method"] == "DELETE"