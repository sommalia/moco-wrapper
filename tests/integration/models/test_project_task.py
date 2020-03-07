from datetime import date
from .. import IntegrationTest

from moco_wrapper.util.response import JsonResponse, EmptyResponse, ListingResponse

class TestProjectTask(IntegrationTest):
    def get_customer(self):
        with self.recorder.use_cassette("TestProjectTask.get_customer"):
            customer_create = self.moco.Company.create(
                "TestProjectTask",
                company_type="customer"
            )

            return customer_create.data
    
    def get_user(self):
        with self.recorder.use_cassette("TestProjectTask.get_user"):
            user = self.moco.User.getlist().items[0]
            return user

    def get_project(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProjectTask.get_project"):
            project_create = self.moco.Project.create(
                "dummy project, test project_task",
                "EUR",
                user.id,
                customer.id,
                finish_date=date(2020, 1, 1),
            )

            return project_create.data

    def test_get(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectTask.test_get"):
            name = "dummy task, test get"
            billable = False
            active = True
            budget = 500
            hourly_rate = 20

            task_create = self.moco.ProjectTask.create(
                project.id,
                name,
                billable=billable,
                active=active,
                budget=budget,
                hourly_rate=hourly_rate
            )

            task_get = self.moco.ProjectTask.get(
                project.id, 
                task_create.data.id
            )

            assert task_create.response.status_code == 200
            assert task_get.response.status_code == 200

            assert isinstance(task_create, JsonResponse)
            assert isinstance(task_get, JsonResponse)

            assert task_get.data.name == name
            assert task_get.data.billable == billable
            assert task_get.data.active == active
            assert task_get.data.budget == budget
            assert task_get.data.hourly_rate == hourly_rate

    def test_getlist(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectTask.test_getlist"):
            task_list = self.moco.ProjectTask.getlist(project.id)

            assert task_list.response.status_code == 200

            assert isinstance(task_list, ListingResponse)

            assert task_list.current_page == 1
            assert task_list.is_last is not None
            assert task_list.next_page is not None
            assert task_list.total is not None
            assert task_list.page_size is not None

    def test_create(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectTask.test_create"):
            name = "dummy task, test create"

            task_create = self.moco.ProjectTask.create(
                project.id,
                name
            )
            
            assert task_create.response.status_code == 200

            assert isinstance(task_create, JsonResponse)

            assert task_create.data.name == name

    def test_create_full(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectTask.test_create_full"):
            name = "dummy task, test create full"
            billable = False
            active = True
            budget = 500
            hourly_rate = 20

            task_create = self.moco.ProjectTask.create(
                project.id,
                name,
                billable=billable,
                active=active,
                budget=budget,
                hourly_rate=hourly_rate
            )

            assert task_create.response.status_code == 200
          
            assert isinstance(task_create, JsonResponse)
          
            assert task_create.data.name == name
            assert task_create.data.billable == billable
            assert task_create.data.active == active
            assert task_create.data.budget == budget
            assert task_create.data.hourly_rate == hourly_rate

    def test_delete(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectTask.test_delete"):
            task_create = self.moco.ProjectTask.create(
                project.id,
                "dummy task, test delete"
            )

            task_delete = self.moco.ProjectTask.delete(
                project.id,
                task_create.data.id,
            )

            assert task_create.response.status_code == 200
            assert task_delete.response.status_code == 204

            assert isinstance(task_delete, EmptyResponse)


    def test_update(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectTask.test_update"):
            name = "dummy task, this task was successfully updated"
            billable = False
            active = True
            budget = 500
            hourly_rate = 20

            task_create = self.moco.ProjectTask.create(
                project.id,
                "dummy task, test update"
            )

            task_update = self.moco.ProjectTask.update(
                project.id,
                task_create.data.id,
                name=name,
                billable=billable,
                active=active,
                budget=budget,
                hourly_rate=hourly_rate
            )

            assert task_create.response.status_code == 200
            assert task_update.response.status_code == 200
          
            assert isinstance(task_create, JsonResponse)
            assert isinstance(task_update, JsonResponse)
          
            assert task_update.data.name == name
            assert task_update.data.billable == billable
            assert task_update.data.active == active
            assert task_update.data.budget == budget
            assert task_update.data.hourly_rate == hourly_rate
            