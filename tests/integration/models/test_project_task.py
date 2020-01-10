
from datetime import date
from .. import IntegrationTest

from moco_wrapper.util.response import JsonResponse, EmptyResponse

class TestProjectTask(IntegrationTest):
    def test_create(self):
        with self.recorder.use_cassette("TestProjectTask.test_create"):
            user_get = self.moco.User.getlist().items[0]
            company_get = self.moco.Company.getlist().items[0]

            project_create = self.moco.Project.create("testproject with tasks", "EUR", date(2022, 1, 1), user_get.id, company_get.id, "TASK_C-1");
            project_task_create = self.moco.ProjectTask.create(project_create.data.id, "generic task")
            project_task_adv_create = self.moco.ProjectTask.create(project_create.data.id, "more advanced task", billable=True, budget=300.5, hourly_rate=20.5)

            assert project_create.response.status_code == 200
            assert project_task_create.response.status_code == 200
            assert project_task_adv_create.response.status_code == 200

            assert isinstance(project_task_adv_create, JsonResponse)
            assert isinstance(project_task_create, JsonResponse)

            assert project_task_adv_create.data.budget == 300.5
            assert project_task_adv_create.data.hourly_rate == 20.5
            assert project_task_create.data.name == "generic task"

    def test_create_inactive_task(self):
        with self.recorder.use_cassette("TestProjectTask.test_create_inactive_task"):
            user_get = self.moco.User.getlist().items[0]
            company_get = self.moco.Company.getlist().items[0]

            project_create = self.moco.Project.create("testproject with tasks", "EUR", date(2022, 1, 1), user_get.id, company_get.id, "TASK_C-2");
            project_task_create = self.moco.ProjectTask.create(project_create.data.id, "inactive task", active=False)

            assert isinstance(project_task_create, JsonResponse)

            assert project_task_create.data.name == "inactive task"
            assert project_task_create.data.active == False
            assert project_task_create.data.billable == True
            

    def test_create_non_billable_task(self):
        with self.recorder.use_cassette("TestProjectTask.test_create_non_billable_task"):
            user_get = self.moco.User.getlist().items[0]
            company_get = self.moco.Company.getlist().items[0]

            project_create = self.moco.Project.create("testproject with tasks", "EUR", date(2022, 1, 1), user_get.id, company_get.id, "TASK_C-3");
            project_task_create = self.moco.ProjectTask.create(project_create.data.id, "non-billable task", billable=False)

            assert isinstance(project_task_create, JsonResponse)

            assert project_task_create.data.name == "non-billable task"
            assert project_task_create.data.active == True
            assert project_task_create.data.billable == False

    def test_delete(self):
        with self.recorder.use_cassette("TestProjectTask.test_delete"):
            user_get = self.moco.User.getlist().items[0]
            company_get = self.moco.Company.getlist().items[0]

            project_create = self.moco.Project.create("testproject with tasks", "EUR", date(2022, 1, 1), user_get.id, company_get.id, "TASK_D-1");
            project_task_create = self.moco.ProjectTask.create(project_create.data.id, "task to delete")
            project_task_delete = self.moco.ProjectTask.delete(project_create.data.id, project_task_create.data.id)

            assert project_create.response.status_code == 200
            assert project_task_create.response.status_code == 200
            assert project_task_delete.response.status_code == 204

            assert isinstance(project_task_delete, EmptyResponse)
