from moco_wrapper.models.schedule import ScheduleAbsenceCode, ScheduleSymbol, ScheduleAssignmentType
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
                name="TestSchedule",
                company_type="customer"
            )

            return customer_create.data

    def test_getlist(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestSchedule.test_getlist"):
            sched_list = self.moco.Schedule.getlist(
                from_date=date(2019, 1, 1),
                to_date=date(2021, 12, 31),
                user_id=user.id,
                absence_code=ScheduleAbsenceCode.UNPLANNED
            )

            assert sched_list.response.status_code == 200

            assert isinstance(sched_list, ListingResponse)

            assert sched_list.current_page == 1
            assert sched_list.is_last is not None
            assert sched_list.next_page is not None
            assert sched_list.total is not None
            assert sched_list.page_size is not None

    def test_create(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestSchedule.test_create_with_absence"):
            sched_create = self.moco.Schedule.create(
                schedule_date=self.create_random_date(),
                absence_code=ScheduleAbsenceCode.HOLIDAY,
                user_id=user.id
            )

            assert sched_create.response.status_code == 200

            assert isinstance(sched_create, JsonResponse)

            assert sched_create.data.assignment.type == ScheduleAssignmentType.ABSENCE
            assert sched_create.data.user.id == user.id

    def test_create_full(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestSchedule.test_create_full"):
            sched_date = date(2020, 1, 1)
            am = False
            pm = True
            comment = "dummy schedule, test create full"
            symbol = ScheduleSymbol.CAR
            overwrite = True
            absence_code = ScheduleAbsenceCode.HOLIDAY

            sched_create = self.moco.Schedule.create(
                schedule_date=sched_date,
                absence_code=absence_code,
                user_id=user.id,
                am=am,
                pm=pm,
                comment=comment,
                overwrite=True,
                symbol=symbol,
            )

            assert sched_create.response.status_code == 200

            assert isinstance(sched_create, JsonResponse)

            assert sched_create.data.date == sched_date.isoformat()
            assert sched_create.data.assignment.type == ScheduleAssignmentType.ABSENCE
            assert sched_create.data.user.id == user.id
            assert sched_create.data.am == am
            assert sched_create.data.pm == pm
            assert sched_create.data.comment == comment

    def test_get(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestSchedule.test_get"):
            sched_date = date(2020, 1, 1)
            am = False
            pm = True
            comment = "dummy schedule, test get"
            symbol = ScheduleSymbol.CAR
            absence_code = ScheduleAbsenceCode.SICK_DAY

            sched_create = self.moco.Schedule.create(
                schedule_date=sched_date,
                absence_code=absence_code,
                user_id=user.id,
                am=am,
                pm=pm,
                comment=comment,
                overwrite=True,
                symbol=symbol
            )

            sched_get = self.moco.Schedule.get(sched_create.data.id)

            assert sched_create.response.status_code == 200
            assert sched_get.response.status_code == 200

            assert isinstance(sched_create, JsonResponse)
            assert isinstance(sched_get, JsonResponse)

            assert sched_get.data.date == sched_date.isoformat()
            assert sched_get.data.assignment.type == ScheduleAssignmentType.ABSENCE
            assert sched_get.data.user.id == user.id
            assert sched_get.data.am == am
            assert sched_get.data.pm == pm
            assert sched_get.data.comment == comment

    def test_update(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestSchedule.test_update"):
            sched_date = self.create_random_date()
            am = False
            pm = True
            comment = "dummy schedule, test update"
            symbol = ScheduleSymbol.CAR
            absence_code = ScheduleAbsenceCode.ABSENCE

            sched_create = self.moco.Schedule.create(
                schedule_date=sched_date,
                absence_code=absence_code,
                user_id=user.id,
                symbol=symbol
            )

            sched_update = self.moco.Schedule.update(
                schedule_id= sched_create.data.id,
                absence_code=absence_code,
                am=am,
                pm=pm,
                comment=comment,
                overwrite=True
            )

            assert sched_create.response.status_code == 200
            assert sched_update.response.status_code == 200

            assert isinstance(sched_create, JsonResponse)
            assert isinstance(sched_update, JsonResponse)

            assert sched_update.data.assignment.type == ScheduleAssignmentType.ABSENCE
            assert sched_update.data.user.id == user.id
            assert sched_update.data.am == am
            assert sched_update.data.pm == pm
            assert sched_update.data.comment == comment

    def test_delete(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestSchedule.test_delete"):
            sched_create = self.moco.Schedule.create(
                schedule_date=self.create_random_date(),
                absence_code=ScheduleAbsenceCode.ABSENCE,
                user_id=user.id
            )

            sched_delete = self.moco.Schedule.delete(sched_create.data.id)

            assert sched_create.response.status_code == 200
            assert sched_delete.response.status_code == 200

            assert isinstance(sched_create, JsonResponse)
            assert isinstance(sched_delete, JsonResponse)
