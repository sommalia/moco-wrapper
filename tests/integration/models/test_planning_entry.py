from .. import IntegrationTest
from moco_wrapper.util.response import ListingResponse, JsonResponse, EmptyResponse
from moco_wrapper.models.company import CompanyType
from moco_wrapper.models.planning_entry import PlanningEntrySymbol
from datetime import date


class TestPlanningEntry(IntegrationTest):
    def get_customer(self):
        with self.recorder.use_cassette("TestPlanningEntry.get_customer"):
            customer = self.moco.Company.create(
                name="Dummy company, planning entry",
                company_type=CompanyType.CUSTOMER
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
                firstname="dummy",
                lastname="user",
                email="{}@mycompany.com".format(self.id_generator()),
                password=self.id_generator(),
                unit_id=unit.id
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

    def test_get(self):
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

    def test_update(self):
        user = self.get_other_user()
        project = self.get_project()

        with self.recorder.use_cassette("TestPlanningEntry.test_update"):
            start_date = date(2020, 1, 1)
            end_date = date(2020, 1, 2)
            hours_per_day = 2.5
            comment = "dummy entry, test update 2"
            symbol = PlanningEntrySymbol.GRADUATION_CAP

            plan_create = self.moco.PlanningEntry.create(
                project.id,
                date(2020, 2, 1),
                date(2020, 2, 2),
                3,
                user_id=user.id,
                comment="dummy comment, test update",
                symbol=PlanningEntrySymbol.HOME
            )

            plan_update = self.moco.PlanningEntry.update(
                plan_create.data.id,
                project_id=project.id,
                starts_on=start_date,
                ends_on=end_date,
                hours_per_day=hours_per_day,
                comment=comment,
                symbol=symbol
            )

            assert plan_create.response.status_code == 200
            assert plan_update.response.status_code == 200

            assert isinstance(plan_create, JsonResponse)
            assert isinstance(plan_update, JsonResponse)

            assert plan_update.data.project is not None
            assert plan_update.data.user is not None

            assert plan_update.data.project.id == project.id
            assert plan_update.data.starts_on == start_date.isoformat()
            assert plan_update.data.ends_on == end_date.isoformat()
            assert plan_update.data.hours_per_day == hours_per_day
            assert plan_update.data.user.id == user.id
            assert plan_update.data.comment == comment
            assert plan_update.data.symbol == symbol

    def test_delete(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestPlanningEntry.test_delete"):
            plan_create = self.moco.PlanningEntry.create(
                project.id,
                date(2020, 1, 1),
                date(2020, 1, 1),
                2
            )

            plan_delete = self.moco.PlanningEntry.delete(plan_create.data.id)

            assert plan_create.response.status_code == 200
            assert plan_delete.response.status_code == 200

            assert isinstance(plan_create, JsonResponse)
            assert isinstance(plan_delete, JsonResponse)

