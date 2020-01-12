from moco_wrapper.util.response import JsonResponse, ListingResponse, EmptyResponse

from .. import IntegrationTest

from datetime import date

class TestActivity(IntegrationTest):
    def test_create(self):
        with self.recorder.use_cassette("TestActivity.test_create"):
            #create the project
            customer_id = self.moco.Company.getlist().items[0].id
            leader_id = self.moco.User.getlist().items[0].id

            project_create = self.moco.Project.create("test project with acitities", "EUR", date(2020, 1, 1), leader_id, customer_id)

            #create the task
            project_task_create = self.moco.ProjectTask.create(project_create.data.id, "task with activity")

            #create the activity
            activity_desc = "another thing i did"
            activity_create = self.moco.Activity.create(date(2020, 1, 1), project_create.data.id, project_task_create.data.id, 0.25, description=activity_desc)

            assert project_create.response.status_code == 200
            assert project_task_create.response.status_code == 200
            assert activity_create.response.status_code == 200

            assert isinstance(activity_create, JsonResponse)

            assert activity_create.data.date == date(2020, 1, 1).isoformat()
            assert activity_create.data.description == activity_desc
    
    def test_create_non_billable(self):
        with self.recorder.use_cassette("TestActivity.test_create_non_billable"):
            #create the project
            customer_id = self.moco.Company.getlist().items[0].id
            leader_id = self.moco.User.getlist().items[0].id

            project_create = self.moco.Project.create("test project with acitities", "EUR", date(2020, 1, 1), leader_id, customer_id)

            #create the task
            project_task_create = self.moco.ProjectTask.create(project_create.data.id, "task with activity")

            #create the activity
            activity_desc = "another thing i did"
            activity_create = self.moco.Activity.create(date(2020, 1, 1), project_create.data.id, project_task_create.data.id, 0.25, description=activity_desc, billable=False)

            assert project_create.response.status_code == 200
            assert project_task_create.response.status_code == 200
            assert activity_create.response.status_code == 200

            assert isinstance(activity_create, JsonResponse)

            assert activity_create.data.date == date(2020, 1, 1).isoformat()
            assert activity_create.data.description == activity_desc
            assert activity_create.data.billable == False

    def test_update(self):
        with self.recorder.use_cassette("TestActivity.test_update"):
            customer_id = self.moco.Company.getlist().items[0].id
            leader_id = self.moco.User.getlist().items[0].id

            project_create = self.moco.Project.create("test project with acitities", "EUR", date(2020, 1, 1), leader_id, customer_id)

            #create the task
            project_task_create = self.moco.ProjectTask.create(project_create.data.id, "task with activity")

            #create the activity
            activity_desc = "another thing i did"
            activity_create = self.moco.Activity.create(date(2020, 1, 1), project_create.data.id, project_task_create.data.id, 0.25, description=activity_desc, billable=False)

            activity_desc_updated = "updated desc"
            activity_update = self.moco.Activity.update(activity_create.data.id, activity_date=date(2021, 1,1), description=activity_desc_updated)

            assert project_create.response.status_code == 200
            assert project_task_create.response.status_code == 200
            assert activity_create.response.status_code == 200
            assert activity_update.response.status_code == 200

            assert isinstance(activity_update, JsonResponse)

            assert activity_update.data.description == activity_desc_updated
            assert activity_update.data.date == date(2021, 1, 1).isoformat()

    def test_getlist(self):
        with self.recorder.use_cassette("TestActivity.test_getlist"):
            activity_getlist = self.moco.Activity.getlist(date(1990, 1, 1), date(2020, 1, 1))
            
            assert activity_getlist.response.status_code == 200

            assert isinstance(activity_getlist, ListingResponse)

    def test_get(self):
        with self.recorder.use_cassette("TestActivity.test_get"):
            customer_id = self.moco.Company.getlist().items[0].id
            leader_id = self.moco.User.getlist().items[0].id

            project_create = self.moco.Project.create("test project with acitities", "EUR", date(2020, 1, 1), leader_id, customer_id)

            #create the task
            project_task_create = self.moco.ProjectTask.create(project_create.data.id, "task with activity")

            #create the activity
            activity_desc = "another thing i did"
            activity_create = self.moco.Activity.create(date(2020, 1, 1), project_create.data.id, project_task_create.data.id, 0.25, description=activity_desc, billable=False)

            activity_get = self.moco.Activity.get(activity_create.data.id)

            assert activity_create.response.status_code == 200
            assert activity_get.response.status_code == 200

            assert isinstance(activity_get, JsonResponse)

    def test_start_timer(self):
        with self.recorder.use_cassette("TestActivity.test_start_timer"):
            customer_id = self.moco.Company.getlist().items[0].id
            leader_id = self.moco.User.getlist().items[0].id
            project_create = self.moco.Project.create("test project with activities", "EUR", date(2020, 1, 1), leader_id, customer_id)

            project_task_create = self.moco.ProjectTask.create(project_create.data.id, "task with activity")

            activity_create = self.moco.Activity.create(date(2021, 1, 1), project_create.data.id, project_task_create.data.id, 0.5)
            timer_start = self.moco.Activity.start_timer(activity_create.data.id)

            assert project_create.response.status_code == 200
            assert project_task_create.response.status_code == 200
            assert activity_create.response.status_code == 200
            assert timer_start.response.status_code == 200

            assert isinstance(timer_start, JsonResponse)


    def test_stop_timer(self):
        with self.recorder.use_cassette("TestActivity.test_stop_timer"):
            customer_id = self.moco.Company.getlist().items[0].id
            leader_id = self.moco.User.getlist().items[0].id
            project_create = self.moco.Project.create("test project with activities", "EUR", date(2020, 1, 1), leader_id, customer_id)

            project_task_create = self.moco.ProjectTask.create(project_create.data.id, "task with activity")

            activity_create = self.moco.Activity.create(date(2021, 1, 1), project_create.data.id, project_task_create.data.id, 0.5)
            timer_start = self.moco.Activity.start_timer(activity_create.data.id)
            timer_stop = self.moco.Activity.stop_timer(activity_create.data.id)

            assert project_create.response.status_code == 200
            assert project_task_create.response.status_code == 200
            assert activity_create.response.status_code == 200
            assert timer_start.response.status_code == 200
            assert timer_stop.response.status_code == 200

            assert isinstance(timer_stop, JsonResponse)

    def test_delete(self):
        with self.recorder.use_cassette("TestActivity.test_delete"):
            customer_id = self.moco.Company.getlist().items[0].id
            leader_id = self.moco.User.getlist().items[0].id
            project_create = self.moco.Project.create("test project with activities", "EUR", date(2020, 1, 1), leader_id, customer_id)

            project_task_create = self.moco.ProjectTask.create(project_create.data.id, "task with activity")

            activity_create = self.moco.Activity.create(date(2021, 1, 1), project_create.data.id, project_task_create.data.id, 0.5)
            activity_delete = self.moco.Activity.delete(activity_create.data.id)

            assert project_create.response.status_code == 200
            assert project_task_create.response.status_code == 200
            assert activity_create.response.status_code == 200
            assert activity_delete.response.status_code == 204

            assert isinstance(activity_delete, EmptyResponse)            

    def test_disregard(self):
        with self.recorder.use_cassette("TestActivity.test_disregard"):
            customer_id = self.moco.Company.getlist().items[0].id
            leader_id = self.moco.User.getlist().items[0].id
            project_create = self.moco.Project.create("test project with activities", "EUR", date(2020, 1, 1), leader_id, customer_id)

            project_task_create = self.moco.ProjectTask.create(project_create.data.id, "task with activity")

            activity_create = self.moco.Activity.create(date(2021, 1, 1), project_create.data.id, project_task_create.data.id, 0.5)
            activity_create_sec = self.moco.Activity.create(date(2021, 1, 1), project_create.data.id, project_task_create.data.id, 1)
            
            disregard_ids = [activity_create.data.id, activity_create_sec.data.id]
            activity_disregard = self.moco.Activity.disregard("tested disregard", disregard_ids, customer_id)

            assert project_create.response.status_code == 200
            assert project_task_create.response.status_code == 200
            assert activity_create.response.status_code == 200
            assert activity_create_sec.response.status_code == 200
            assert activity_disregard.response.status_code == 200