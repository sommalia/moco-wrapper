from moco_wrapper.models.schedule import ScheduleAbsenceCode, ScheduleSymbol
from moco_wrapper.util.response import JsonResponse, ListingResponse, EmptyResponse

from datetime import date
from .. import IntegrationTest

class TestSchedule(IntegrationTest):
    def get_user(self):
        with self.recorder.use_cassette("TestSchedule.get_user"):
            user = self.moco.User.getlist().items[0]
            return user

    def get_customer(self):
        with self.recorder.use_cassette("TestSchedule.get_customer"):
            customer_create = self.moco.Company.create(
                "TestSchedule",
                company_type="customer"
            )

            return customer_create.data
    
    def get_project(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestSchedule.get_project"):
            project_create = self.moco.Project.create(
                "dummy project, test schedules",
                "EUR",
                date(2020, 1, 1),
                user.id,
                customer.id
            )

            return project_create.data

    def test_getlist(self):
        user = self.get_user()
        project = self.get_project()

        with self.recorder.use_cassette("TestSchedule.test_getlist"):
            sched_list = self.moco.Schedule.getlist(
                from_date=date(2019, 1, 1),
                to_date=date(2021, 12, 31),
                user_id=user.id,
                absence_code=ScheduleAbsenceCode.UNPLANNED,
                project_id=project.id,
            )

            assert sched_list.response.status_code == 200

            assert isinstance(sched_list, ListingResponse)