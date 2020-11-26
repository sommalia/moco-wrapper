from moco_wrapper.models.activity import ActivityRemoteService
from moco_wrapper.models.company import CompanyType
from moco_wrapper.util.response import ObjectResponse, PagedListResponse, EmptyResponse
from datetime import date

from .. import IntegrationTest


class TestActivity(IntegrationTest):

    def get_customer(self):
        with self.recorder.use_cassette("TestActivity.get_customer"):
            customer_create = self.moco.Company.create(
                name="TestActivity.get_customer",
                company_type=CompanyType.CUSTOMER
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
                name="TestActivity.get_project",
                currency="EUR",
                leader_id=user.id,
                customer_id=customer.id,
                finish_date=date(2020, 1, 1),
            )

            return project_create.data

    def get_project_task(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestActivity.get_project_task"):
            project_task_create = self.moco.ProjectTask.create(
                project_id=project.id,
                name="TestActivity.get_project_task"
            )

            return project_task_create.data

    def get_other_user(self):
        unit = self.get_unit()
        project = self.get_project()

        with self.recorder.use_cassette("TestActivity.get_other_user"):
            user_create = self.moco.User.create(
                firstname="John",
                lastname="Doe",
                email="{}@example.org".format(self.id_generator()),
                password=self.id_generator(),
                unit_id=unit.id
            )

            project_contract_create = self.moco.ProjectContract.create(
                project_id=project.id,
                user_id=user_create.data.id,
                active=True
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
            description = "TestActivity.test_create"

            # impersonate the user that created the project
            self.moco.impersonate(project.leader.id)

            # create the activity
            activity_create = self.moco.Activity.create(
                activity_date=activity_date,
                project_id=project.id,
                task_id=task.id,
                hours=hours,
                description=description,
            )

            # clear impersonation
            self.moco.clear_impersonation()

            assert activity_create.response.status_code == 200

            assert type(activity_create) is ObjectResponse

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
            description = "TestActivity.test_create_full"
            billable = True
            tag = "test_activity"
            remote_service = ActivityRemoteService.JIRA
            remote_id = "JIRA-123"
            remote_url = "https://jira.example.org"

            # impersonate the user that created the project
            self.moco.impersonate(project.leader.id)

            # create the activity
            activity_create = self.moco.Activity.create(
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

            # clear impersonation
            self.moco.clear_impersonation()

            assert activity_create.response.status_code == 200

            assert type(activity_create) is ObjectResponse

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
            description = "TestActivity.test_update"
            billable = True
            tag = "test_activity"
            remote_service = ActivityRemoteService.JIRA
            remote_id = "JIRA-123"
            remote_url = "https://jira.example.org"

            # impersonate the user that created the project
            self.moco.impersonate(project.leader.id)

            # create the activity
            activity_create = self.moco.Activity.create(
                activity_date=date(2019, 12, 31),
                project_id=project.id,
                task_id=task.id,
                hours=2.3,
                description="TestActivity.test_update_create"
            )

            # update the activity
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

            # clear impersonation
            self.moco.clear_impersonation()

            assert activity_create.response.status_code == 200
            assert activity_update.response.status_code == 200

            assert type(activity_create) is  ObjectResponse
            assert type(activity_update) is ObjectResponse

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

            activity_getlist = self.moco.Activity.getlist(
                from_date=from_date,
                to_date=to_date
            )

            assert activity_getlist.response.status_code == 200

            assert type(activity_getlist) is PagedListResponse

            assert activity_getlist.current_page == 1
            assert activity_getlist.is_last is not None
            assert activity_getlist.next_page is not None
            assert activity_getlist.total is not None
            assert activity_getlist.page_size is not None

    def test_getlist_with_task(self):
        project = self.get_project()
        task = self.get_project_task()

        with self.recorder.use_cassette("TestActivity.test_getlist_with_task"):
            from_date = date(1990, 1, 1)
            to_date = date(2020, 1, 1)

            activity_getlist = self.moco.Activity.getlist(
                from_date=from_date,
                to_date=to_date,
                task_id=task.id,
                project_id=project.id
            )

            assert activity_getlist.response.status_code == 200

            assert type(activity_getlist) is PagedListResponse

            assert activity_getlist.current_page == 1
            assert activity_getlist.is_last is not None
            assert activity_getlist.next_page is not None
            assert activity_getlist.total is not None
            assert activity_getlist.page_size is not None

    def test_get(self):
        customer = self.get_customer()
        project = self.get_project()
        task = self.get_project_task()

        with self.recorder.use_cassette("TestActivity.test_get"):
            activity_date = date(2020, 1, 1)
            hours = 3.5
            description = "TestActivity.test_get"
            billable = True
            tag = "test_activity"
            remote_service = ActivityRemoteService.JIRA
            remote_id = "JIRA-123"
            remote_url = "https://jira.example.org"

            # impersonate the user that created the project
            self.moco.impersonate(project.leader.id)

            # create the activity
            activity_create = self.moco.Activity.create(
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

            activity_get = self.moco.Activity.get(activity_create.data.id)

            # clear impersonation
            self.moco.clear_impersonation()

            assert activity_create.response.status_code == 200
            assert activity_get.response.status_code == 200

            assert type(activity_create) is ObjectResponse
            assert type(activity_get) is ObjectResponse

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
            self.moco.impersonate(project.leader.id)

            activity_create = self.moco.Activity.create(
                activity_date=date.today(),
                project_id=project.id,
                task_id=task.id,
                hours=0.5,
                description="TestActivity.test_start_timer_create"
            )

            timer_start = self.moco.Activity.start_timer(
                activity_id=activity_create.data.id
            )

            self.moco.clear_impersonation()

            assert activity_create.response.status_code == 200
            assert timer_start.response.status_code == 200

            assert type(timer_start) is ObjectResponse

    def test_stop_timer(self):
        project = self.get_project()
        task = self.get_project_task()

        with self.recorder.use_cassette("TestActivity.test_stop_timer"):
            self.moco.impersonate(project.leader.id)

            activity_create = self.moco.Activity.create(
                activity_date=date.today(),
                project_id=project.id,
                task_id=task.id,
                hours=0.5,
                description="TestActivity.test_stop_timer_create")

            # start and stop the timer
            timer_start = self.moco.Activity.start_timer(
                activity_id=activity_create.data.id
            )
            timer_stop = self.moco.Activity.stop_timer(
                activity_id=activity_create.data.id
            )

            self.moco.clear_impersonation()

            assert activity_create.response.status_code == 200
            assert timer_start.response.status_code == 200
            assert timer_stop.response.status_code == 200

            assert type(timer_stop) is ObjectResponse

    def test_delete(self):
        project = self.get_project()
        task = self.get_project_task()

        with self.recorder.use_cassette("TestActivity.test_delete"):
            # impersonate the user that created the project
            self.moco.impersonate(project.leader.id)

            activity_create = self.moco.Activity.create(
                activity_date=date(2020, 1, 1),
                project_id=project.id,
                task_id=task.id,
                hours=0.5,
                description="TestActivity.test_delete_create"
            )

            activity_delete = self.moco.Activity.delete(
                activity_id=activity_create.data.id
            )

            self.moco.clear_impersonation()

            assert activity_create.response.status_code == 200
            assert activity_delete.response.status_code == 204

            assert type(activity_delete) is EmptyResponse

    def test_disregard(self):
        customer = self.get_customer()
        project = self.get_project()
        task = self.get_project_task()

        with self.recorder.use_cassette("TestActivity.test_disregard"):
            # impersonate the user that created the project
            self.moco.impersonate(project.leader.id)

            activity_create = self.moco.Activity.create(
                activity_date=date(2021, 1, 1),
                project_id=project.id,
                task_id=task.id,
                hours=0.5,
                description="TestActivity.test_disregard_create_1"
            )

            activity_create_sec = self.moco.Activity.create(
                activity_date=date(2021, 1, 1),
                project_id=project.id,
                task_id=task.id,
                hours=1,
                description="TestActivity.test_disregard_create_2"
            )

            self.moco.clear_impersonation()

            disregard_ids = [activity_create.data.id, activity_create_sec.data.id]
            activity_disregard = self.moco.Activity.disregard(
                reason="TestActivity.test_disregard",
                activity_ids=disregard_ids,
                company_id=project.customer.id
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
                activity_date=date(2020, 1, 1),
                project_id=project.id,
                task_id=task.id,
                hours=2,
                description="TestActivity.test_create_impersonate"
            )

            assert activity_create.response.status_code == 200

            assert type(activity_create) is ObjectResponse

            assert activity_create.data.user.id == other_user.id

            self.moco.clear_impersonation()
