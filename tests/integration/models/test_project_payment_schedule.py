from .. import IntegrationTest
from datetime import date

from moco_wrapper.util.response import ObjectResponse, ListResponse, EmptyResponse
from moco_wrapper.models.company import CompanyType


class TestProjectPaymentSchedule(IntegrationTest):
    def get_customer(self):
        with self.recorder.use_cassette("TestProjectPaymentSchedule.get_customer"):
            customer_create = self.moco.Company.create(
                name="TestProjectPaymentSchedule.get_customer",
                company_type=CompanyType.CUSTOMER
            )

            return customer_create.data

    def get_user(self):
        with self.recorder.use_cassette("TestProjectPaymentSchedule.get_user"):
            user = self.moco.User.getlist()[0]
            return user

    def get_project(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProjectPaymentSchedule.get_project"):
            project_create = self.moco.Project.create(
                name="TestProjectPaymentSchedule.get_project",
                currency="EUR",
                leader_id=user.id,
                customer_id=customer.id,
                fixed_price=True,
                budget=1000.0
            )

            return project_create.data

    def test_getlist(self):
        project = self.get_project()
        from_date = date(2021, 2, 23)
        to_date = date(2023, 2, 2)
        checked = False

        with self.recorder.use_cassette("TestProjectPaymentSchedule.test_getlist"):
            sched_list = self.moco.ProjectPaymentSchedule.getlist(
                project_id=project.id,
                from_date=from_date,
                to_date=to_date,
                checked=checked
            )

            assert sched_list.response.status_code == 200

            assert type(sched_list) is ListResponse


    def test_getall(self):
        customer = self.get_customer()
        from_date = date(2021, 2, 23)
        to_date = date(2023, 2, 2)
        checked = True

        with self.recorder.use_cassette("TestProjectPaymentSchedule.test_getall"):
            sched_list = self.moco.ProjectPaymentSchedule.getall(
                company_id=customer.id,
                from_date=from_date,
                to_date=to_date,
                checked=checked
            )

            assert sched_list.response.status_code == 200

            assert type(sched_list) is ListResponse

    def test_get(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectPaymentSchedule.test_get"):
            net_total = 100
            sched_date = date(2020, 1, 1)
            title = "TestProjectPaymentSchedule.test_get_create"
            checked = True

            sched_create = self.moco.ProjectPaymentSchedule.create(
                project_id=project.id,
                net_total=net_total,
                schedule_date=sched_date,
                title=title,
                checked=checked
            )

            sched_get = self.moco.ProjectPaymentSchedule.get(
                project_id=project.id,
                schedule_id=sched_create.data.id
            )

            assert sched_create.response.status_code == 200
            assert sched_get.response.status_code == 200

            assert type(sched_create) is ObjectResponse
            assert type(sched_get) is ObjectResponse

            assert sched_get.data.date == sched_date.isoformat()
            assert sched_get.data.net_total == net_total
            assert sched_get.data.project.id == project.id
            assert sched_get.data.title == title
            assert sched_get.data.checked == checked

    def test_create(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectPaymentSchedule.test_create"):
            net_total = 100
            sched_date = date(2020, 1, 1)

            sched_create = self.moco.ProjectPaymentSchedule.create(
                project_id=project.id,
                net_total=net_total,
                schedule_date=sched_date
            )

            assert sched_create.response.status_code == 200

            assert type(sched_create) is ObjectResponse

            assert sched_create.data.date == sched_date.isoformat()
            assert sched_create.data.net_total == net_total
            assert sched_create.data.project.id == project.id

    def test_create_full(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectPaymentSchedule.test_create_full"):
            net_total = 100
            sched_date = date(2020, 1, 1)
            title = "TestProjectPaymentSchedule.test_create_full"
            checked = True

            sched_create = self.moco.ProjectPaymentSchedule.create(
                project_id=project.id,
                net_total=net_total,
                schedule_date=sched_date,
                title=title,
                checked=checked
            )

            assert sched_create.response.status_code == 200

            assert type(sched_create) is ObjectResponse

            assert sched_create.data.date == sched_date.isoformat()
            assert sched_create.data.net_total == net_total
            assert sched_create.data.project.id == project.id
            assert sched_create.data.title == title
            assert sched_create.data.checked == checked

    def test_update(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectPaymentSchedule.test_update"):
            net_total = 100
            sched_date = date(2020, 3, 1)
            title = "TestProjectPaymentSchedule.test_update"
            checked = True

            sched_create = self.moco.ProjectPaymentSchedule.create(
                project_id=project.id,
                net_total=1,
                schedule_date=date(2020, 12, 1)
            )

            sched_update = self.moco.ProjectPaymentSchedule.update(
                project_id=project.id,
                schedule_id=sched_create.data.id,
                net_total=net_total,
                schedule_date=sched_date,
                title=title,
                checked=checked
            )

            assert sched_create.response.status_code == 200
            assert sched_update.response.status_code == 200

            assert type(sched_create) is ObjectResponse
            assert type(sched_update) is ObjectResponse

            assert sched_update.data.date == sched_date.isoformat()
            assert sched_update.data.net_total == net_total
            assert sched_update.data.project.id == project.id
            assert sched_update.data.title == title
            assert sched_update.data.checked == checked

    def test_delete(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectPaymentSchedule.test_delete"):
            sched_create = self.moco.ProjectPaymentSchedule.create(
                project_id=project.id,
                net_total=1,
                schedule_date=date(2020, 12, 1)
            )

            sched_delete = self.moco.ProjectPaymentSchedule.delete(
                project_id=project.id,
                schedule_id=sched_create.data.id
            )

            assert sched_create.response.status_code == 200
            assert sched_delete.response.status_code == 200

            assert type(sched_create) is ObjectResponse
            assert type(sched_delete) is ObjectResponse
