from moco_wrapper.util.response import JsonResponse, ListingResponse, EmptyResponse
from moco_wrapper.models.activity import ActivityRemoteService
from datetime import date

from .. import IntegrationTest

class TestActivity(IntegrationTest):

    def get_customer(self):
        with self.recorder.use_cassette("TestActivity.get_customer"):
            customer_create = self.moco.Company.create(
                "TestActivity",
                company_type="customer"
            )

            return customer_create.data

    def get_user(self):
        with self.recorder.use_cassette("TestActivity.get_user"):
            user = self.moco.User.getlist().items[0]
            return user

    def get_project(self):
        customer = self.get_customer()
        user = self.get_user()

        with self.recorder.use_cassette("TestActivity.get_project"):
            project_create = self.moco.Project.create(
                "project created for testing activities", 
                "EUR", 
                user.id, 
                customer.id,
                finish_date = date(2020, 1, 1), 
            )

            return project_create.data

    def get_project_task(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestActivity.get_project_task"):
            project_task_create = self.moco.ProjectTask.create(
                project.id,
                "project task created for testing activities"
                )
            
            return project_task_create.data


    def get_other_user(self):
        unit = self.get_unit()
        project = self.get_project()

        with self.recorder.use_cassette("TestActivity.get_other_user"):
            user_create = self.moco.User.create(
                "Test",
                "Impersonation",
                "{}@mycompany.com".format(self.id_generator()),
                self.id_generator(),
                unit.id
            )

            project_contract_create = self.moco.ProjectContract.create(
                project.id,
                user_create.data.id
            )

            return user_create.data

    def get_unit(self):
        with self.recorder.use_cassette("TestActivity.get_unit"):
            unit = self.moco.Unit.getlist().items[0]
            return unit

    def test_create(self):
        customer = self.get_customer()
        project = self.get_project()
        task = self.get_project_task()

        with self.recorder.use_cassette("TestActivity.test_create"):
            activity_date = date(2020, 1, 1)
            hours = 3.5
            description = "activity create description"
            
            #create the activity
            activity_create = self.moco.Activity.create(
                activity_date,
                project.id,
                task.id,
                hours,
                description=description,
            )

            assert activity_create.response.status_code == 200

            assert isinstance(activity_create, JsonResponse)

            assert activity_create.data.date == activity_date.isoformat()
            assert activity_create.data.description == description
            assert activity_create.data.project.id == project.id
            assert activity_create.data.task.id == task.id
            assert activity_create.data.hours == hours
            assert activity_create.data.customer.id == customer.id
            assert activity_create.data.user.id is not None
    
    def test_create_full(self):
        customer = self.get_customer()
        project = self.get_project()
        task = self.get_project_task()

        with self.recorder.use_cassette("TestActivity.test_create_full"):
            activity_date = date(2020, 1, 1)
            hours = 3.5
            description = "activity create description"
            billable = True
            tag = "test_activity"
            remote_service = ActivityRemoteService.JIRA
            remote_id = "JIRA-123"
            remote_url = "https://jira.mycompany.com"
            
            #create the activity
            activity_create = self.moco.Activity.create(
                activity_date,
                project.id,
                task.id,
                hours,
                description=description,
                billable=billable,
                tag=tag,
                remote_service=remote_service,
                remote_id=remote_id,
                remote_url=remote_url,
            )

            assert activity_create.response.status_code == 200

            assert isinstance(activity_create, JsonResponse)

            assert activity_create.data.date == activity_date.isoformat()
            assert activity_create.data.description == description
            assert activity_create.data.project.id == project.id
            assert activity_create.data.task.id == task.id
            assert activity_create.data.hours == hours
            assert activity_create.data.billable == billable
            assert activity_create.data.tag == tag
            assert activity_create.data.remote_service == remote_service
            assert activity_create.data.remote_id == remote_id
            assert activity_create.data.remote_url == remote_url
            assert activity_create.data.customer.id == customer.id
            assert activity_create.data.user.id is not None

    def test_update(self):
        customer = self.get_customer()
        project = self.get_project()
        task = self.get_project_task()

        with self.recorder.use_cassette("TestActivity.test_update"):
            activity_date = date(2020, 1, 1)
            hours = 3.5
            description = "activity create description"
            billable = True
            tag = "test_activity"
            remote_service = ActivityRemoteService.JIRA
            remote_id = "JIRA-123"
            remote_url = "https://jira.mycompany.com"
            
            #create the activity
            activity_create = self.moco.Activity.create(
                date(2019, 12, 31), 
                project.id, 
                task.id, 
                2.3, 
                description="dummy activity, test_update"
            )
            
            #update the activity
            activity_update = self.moco.Activity.update(
                activity_create.data.id,
                activity_date=activity_date,
                project_id=project.id,
                task_id=task.id,
                hours=hours,
                description=description,
                billable=billable,
                tag=tag,
                remote_service=remote_service,
                remote_id=remote_id,
                remote_url=remote_url,
            )

            assert activity_create.response.status_code == 200
            assert activity_update.response.status_code == 200

            assert isinstance(activity_create, JsonResponse)
            assert isinstance(activity_update, JsonResponse)

            assert activity_update.data.date == activity_date.isoformat()
            assert activity_update.data.description == description
            assert activity_update.data.project.id == project.id
            assert activity_update.data.task.id == task.id
            assert activity_update.data.hours == hours
            assert activity_update.data.billable == billable
            assert activity_update.data.tag == tag
            assert activity_update.data.remote_service == remote_service
            assert activity_update.data.remote_id == remote_id
            assert activity_update.data.remote_url == remote_url
            assert activity_update.data.customer.id == customer.id
            assert activity_update.data.user.id is not None

    def test_getlist(self):
        with self.recorder.use_cassette("TestActivity.test_getlist"):
            from_date = date(1990, 1, 1)
            to_date = date(2020, 1, 1)
            activity_getlist = self.moco.Activity.getlist(from_date, to_date)
            
            assert activity_getlist.response.status_code == 200

            assert isinstance(activity_getlist, ListingResponse)

    def test_getlist_with_task(self):
        with self.recorder.use_cassette("TestActivity.test_getlist_with_task"):
            project = self.get_project()
            task = self.get_project_task()


            from_date = date(1990, 1, 1)
            to_date = date(2020, 1, 1)
            activity_getlist = self.moco.Activity.getlist(from_date, to_date, task_id=task.id, project_id=project.id)

            assert activity_getlist.response.status_code == 200

            assert isinstance(activity_getlist, ListingResponse)

    def test_get(self):
        customer = self.get_customer()
        project = self.get_project()
        task = self.get_project_task()

        with self.recorder.use_cassette("TestActivity.test_get"):
            activity_date = date(2020, 1, 1)
            hours = 3.5
            description = "activity create description"
            billable = True
            tag = "test_activity"
            remote_service = ActivityRemoteService.JIRA
            remote_id = "JIRA-123"
            remote_url = "https://jira.mycompany.com"
    
            #create the activity
            activity_create = self.moco.Activity.create(
                activity_date,
                project.id,
                task.id,
                hours,
                description=description,
                billable=billable,
                tag=tag,
                remote_service=remote_service,
                remote_id=remote_id,
                remote_url=remote_url,
            )

            activity_get = self.moco.Activity.get(activity_create.data.id)

            assert activity_create.response.status_code == 200
            assert activity_get.response.status_code == 200

            assert isinstance(activity_create, JsonResponse)
            assert isinstance(activity_get, JsonResponse)

            assert activity_get.data.date == activity_date.isoformat()
            assert activity_get.data.description == description
            assert activity_get.data.project.id == project.id
            assert activity_get.data.task.id == task.id
            assert activity_get.data.hours == hours
            assert activity_get.data.billable == billable
            assert activity_get.data.tag == tag
            assert activity_get.data.remote_service == remote_service
            assert activity_get.data.remote_id == remote_id
            assert activity_get.data.remote_url == remote_url
            assert activity_get.data.customer.id == customer.id
            assert activity_get.data.user.id is not None

    def test_start_timer(self):
        project = self.get_project()
        task = self.get_project_task()

        with self.recorder.use_cassette("TestActivity.test_start_timer"):
            activity_create = self.moco.Activity.create(
                date(2021, 1, 1), 
                project.id, 
                task.id, 
                0.5,
                description="dummy activity, test_start_timer"
            )

            timer_start = self.moco.Activity.start_timer(activity_create.data.id)

            assert activity_create.response.status_code == 200
            assert timer_start.response.status_code == 200

            assert isinstance(timer_start, JsonResponse)


    def test_stop_timer(self):
        project = self.get_project()
        task = self.get_project_task()

        with self.recorder.use_cassette("TestActivity.test_stop_timer"):
            activity_create = self.moco.Activity.create(
                date(2021, 1, 1), 
                project.id, 
                task.id, 
                0.5,
                description="dummy activity, stop timer")

            timer_start = self.moco.Activity.start_timer(activity_create.data.id)
            timer_stop = self.moco.Activity.stop_timer(activity_create.data.id)

            assert activity_create.response.status_code == 200
            assert timer_start.response.status_code == 200
            assert timer_stop.response.status_code == 200

            assert isinstance(timer_stop, JsonResponse)

    def test_delete(self):
        project = self.get_project()
        task = self.get_project_task()

        with self.recorder.use_cassette("TestActivity.test_delete"):
            activity_create = self.moco.Activity.create(
                date(2020, 1, 1),
                project.id,
                task.id,
                0.5,
                description="dummy activity, test delete"
            )

            activity_delete = self.moco.Activity.delete(activity_create.data.id)

            assert activity_create.response.status_code == 200
            assert activity_delete.response.status_code == 204

            assert isinstance(activity_delete, EmptyResponse)            

    def test_disregard(self):
        customer = self.get_customer()
        project = self.get_project()    
        task = self.get_project_task()

        with self.recorder.use_cassette("TestActivity.test_disregard"):
            activity_create = self.moco.Activity.create(
                date(2021, 1, 1), 
                project.id, 
                task.id, 
                0.5,
                description="dummy activity, disregard (1)"
            )

            activity_create_sec = self.moco.Activity.create(
                date(2021, 1, 1), 
                project.id, 
                task.id, 
                1,
                description="dummy activity, disregard (2)"
            )
            
            disregard_ids = [activity_create.data.id, activity_create_sec.data.id]
            activity_disregard = self.moco.Activity.disregard(
                "tested disregard", 
                disregard_ids, 
                project.customer.id 
            )

            assert activity_create.response.status_code == 200
            assert activity_create_sec.response.status_code == 200
            assert activity_disregard.response.status_code == 200

    def test_create_impersonate(self):
        other_user = self.get_other_user()
        project = self.get_project()
        task = self.get_project_task()

        with self.recorder.use_cassette("TestActivity.test_create_impersonate"):

            self.moco.impersonate(other_user.id)

            activity_create = self.moco.Activity.create(
                date(2020, 1, 1),
                project.id,
                task.id,
                2,
                description="dummy description, test impersonate"
            )

            assert activity_create.response.status_code == 200
            
            assert isinstance(activity_create, JsonResponse)

            assert activity_create.data.user.id == other_user.id

            self.moco.clear_impersonation()

