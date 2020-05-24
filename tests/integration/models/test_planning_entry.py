from .. import IntegrationTest
from moco_wrapper.util.response import ListingResponse, JsonResponse
from moco_wrapper.models.company import CompanyType
from moco_wrapper.models.planning_entry import PlanningEntrySymbol
from datetime import date


class TestPlanningEntry(IntegrationTest):
    def get_customer(self):
        with self.recorder.use_cassette("TestPlanningEntry.get_customer"):
            customer = self.moco.Company.create(
                "Dummy company, planning entry",
                CompanyType.CUSTOMER
            )

            return customer.data

    def get_user(self):
        with self.recorder.use_cassette("TestPlanningEntry.get_user"):
            user = self.moco.User.getlist().items[0]
            return user

    def get_unit(self):
        with self.recorder.use_cassette("TestPlanningEntry.get_unit"):
            unit = self.moco.Unit.getlist().items[0]
            return unit

    def get_other_user(self):
        unit = self.get_unit()

        with self.recorder.use_cassette("TestPlanningEntry.get_other_user"):
            user = self.moco.User.create(
                "dummy",
                "user",
                "dummy.user@mycompany.com",
                self.id_generator(),
                unit.id
            )

            return user.data

    def get_project(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestPlanningEntry.get_project"):
            project = self.moco.Project.create(
                "Dummy Project, planning entry",
                "EUR",
                user.id,
                customer.id
            )

            return project.data

    def test_getlist(self):
        with self.recorder.use_cassette("TestPlanningEntry.test_getlist"):
            plan_list = self.moco.PlanningEntry.getlist()

            assert plan_list.response.status_code == 200

            assert isinstance(plan_list, ListingResponse)

            assert plan_list.current_page == 1
            assert plan_list.is_last is not None
            assert plan_list.next_page is not None
            assert plan_list.total is not None
            assert plan_list.page_size is not None

    def test_create(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestPlanningEntry.test_create"):
            start_date = date(2020, 1, 1)
            end_date = date(2020, 1, 2)
            hours_per_day = 2.5

            plan_create = self.moco.PlanningEntry.create(
                project.id,
                start_date,
                end_date,
                hours_per_day
            )

            assert plan_create.response.status_code == 200

            assert isinstance(plan_create, JsonResponse)

            assert plan_create.data.project is not None
            assert plan_create.data.user is not None

            assert plan_create.data.project.id == project.id
            assert plan_create.data.starts_on == start_date.isoformat()
            assert plan_create.data.ends_on == end_date.isoformat()
            assert plan_create.data.hours_per_day == hours_per_day

    def test_create_full(self):
        user = self.get_other_user()
        project = self.get_project()

        with self.recorder.use_cassette("TestPlanningEntry.test_get"):
            start_date = date(2020, 1, 1)
            end_date = date(2020, 1, 2)
            hours_per_day = 2.5
            comment = "dummy entry, test get"
            symbol = PlanningEntrySymbol.GRADUATION_CAP

            plan_create = self.moco.PlanningEntry.create(
                project.id,
                start_date,
                end_date,
                hours_per_day,
                user_id=user.id,
                comment=comment,
                symbol=symbol
            )

            plan_get = self.moco.PlanningEntry.get(
                plan_create.data.id
            )

            assert plan_create.response.status_code == 200
            assert plan_get.response.status_code == 200

            assert isinstance(plan_create, JsonResponse)
            assert isinstance(plan_get, JsonResponse)

            assert plan_get.data.project is not None
            assert plan_get.data.user is not None

            assert plan_get.data.project.id == project.id
            assert plan_get.data.starts_on == start_date.isoformat()
            assert plan_get.data.ends_on == end_date.isoformat()
            assert plan_get.data.hours_per_day == hours_per_day
            assert plan_get.data.user.id == user.id
            assert plan_get.data.comment == comment
            assert plan_get.data.symbol == symbol

    def test_create_full(self):
        user = self.get_other_user()
        project = self.get_project()

        with self.recorder.use_cassette("TestPlanningEntry.test_create_full"):
            start_date = date(2020, 1, 1)
            end_date = date(2020, 1, 2)
            hours_per_day = 2.5
            comment = "this is the comment text"
            symbol = PlanningEntrySymbol.GRADUATION_CAP

            plan_create = self.moco.PlanningEntry.create(
                project.id,
                start_date,
                end_date,
                hours_per_day,
                user_id=user.id,
                comment=comment,
                symbol=symbol
            )

            assert plan_create.response.status_code == 200

            assert isinstance(plan_create, JsonResponse)

            assert plan_create.data.project is not None
            assert plan_create.data.user is not None

            assert plan_create.data.project.id == project.id
            assert plan_create.data.starts_on == start_date.isoformat()
            assert plan_create.data.ends_on == end_date.isoformat()
            assert plan_create.data.hours_per_day == hours_per_day
            assert plan_create.data.user.id == user.id
            assert plan_create.data.comment == comment
            assert plan_create.data.symbol == symbol
