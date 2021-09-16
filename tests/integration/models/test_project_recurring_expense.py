from moco_wrapper.util.response import PagedListResponse, ObjectResponse, EmptyResponse
from moco_wrapper.models.project_recurring_expense import ProjectRecurringExpensePeriod
from moco_wrapper.models.company import CompanyType

from datetime import date
from .. import IntegrationTest


class TestProjectRecurringExpense(IntegrationTest):
    def get_customer(self):
        with self.recorder.use_cassette("TestProjectRecurringExpense.get_customer"):
            customer_create = self.moco.Company.create(
                name="TestProjectRecurringExpense.get_customer",
                company_type=CompanyType.CUSTOMER
            )

            return customer_create.data

    def get_user(self):
        with self.recorder.use_cassette("TestProjectRecurringExpense.get_user"):
            user = self.moco.User.getlist()[0]
            return user

    def get_project(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProjectRecurringExpense.get_project"):
            project_create = self.moco.Project.create(
                name="TestProjectRecurringExpense.get_project",
                currency="EUR",
                leader_id=user.id,
                customer_id=customer.id,
                finish_date=date(2020, 1, 1),
                budget=10000
            )

            return project_create.data

    def test_getlist(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectRecurringExpense.test_getlist"):
            recexp_list = self.moco.ProjectRecurringExpense.getlist(
                project_id=project.id
            )

            assert recexp_list.response.status_code == 200

            assert type(recexp_list) is PagedListResponse

            assert recexp_list.current_page == 1
            assert recexp_list.is_last is not None
            assert recexp_list.next_page is not None
            assert recexp_list.total is not None
            assert recexp_list.page_size is not None

    def test_create(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectRecurringExpense.test_create"):
            start_date = date(2020, 1, 1)
            period = ProjectRecurringExpensePeriod.BIWEEKLY
            title = "TestProjectRecurringExpense.test_create"
            quantity = 1.5
            unit = "h"
            unit_price = 32.5
            unit_cost = 20.5

            recexp_create = self.moco.ProjectRecurringExpense.create(
                project_id=project.id,
                start_date=start_date,
                period=period,
                title=title,
                quantity=quantity,
                unit=unit,
                unit_price=unit_price,
                unit_cost=unit_cost,
            )

            assert recexp_create.response.status_code == 200

            assert type(recexp_create) is ObjectResponse

            assert recexp_create.data.start_date == start_date.isoformat()
            assert recexp_create.data.period == period
            assert recexp_create.data.quantity == quantity
            assert recexp_create.data.unit == unit
            assert recexp_create.data.unit_price == unit_price
            assert recexp_create.data.unit_cost == unit_cost

    def test_create_full(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectRecurringExpense.test_create_full"):
            start_date = date(2020, 1, 1)
            period = ProjectRecurringExpensePeriod.BIWEEKLY
            title = "TestProjectRecurringExpense.test_create_full"
            quantity = 1.5
            unit = "h"
            unit_price = 32.5
            unit_cost = 20.5
            finish_date = date(2021, 1, 1)
            description = "dummy recurring expense, test create full"
            billable = False
            budget_relevant = True

            recexp_create = self.moco.ProjectRecurringExpense.create(
                project_id=project.id,
                start_date=start_date,
                period=period,
                title=title,
                quantity=quantity,
                unit=unit,
                unit_price=unit_price,
                unit_cost=unit_cost,
                finish_date=finish_date,
                description=description,
                billable=billable,
                budget_relevant=budget_relevant,
            )

            assert recexp_create.response.status_code == 200

            assert type(recexp_create) is ObjectResponse

            assert recexp_create.data.start_date == start_date.isoformat()
            assert recexp_create.data.period == period
            assert recexp_create.data.quantity == quantity
            assert recexp_create.data.unit == unit
            assert recexp_create.data.unit_price == unit_price
            assert recexp_create.data.unit_cost == unit_cost
            assert recexp_create.data.finish_date == finish_date.isoformat()
            assert recexp_create.data.description == description
            assert recexp_create.data.billable == billable
            assert recexp_create.data.budget_relevant == budget_relevant

    def test_update(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectRecurringExpense.test_update"):
            start_date = date(2020, 1, 1)
            period = ProjectRecurringExpensePeriod.BIWEEKLY
            title = "TestProjectRecurringExpense.test_update"
            quantity = 1.5
            unit = "h"
            unit_price = 32.5
            unit_cost = 20.5
            finish_date = date(2040, 1, 1)
            description = "dummy recurring expense, test update"
            billable = False
            budget_relevant = True

            recexp_create = self.moco.ProjectRecurringExpense.create(
                project_id=project.id,
                start_date=start_date,
                period=period,
                title="TestProjectRecurringExpense.test_update_create",
                quantity=1,
                unit="h",
                unit_price=2,
                unit_cost=1
            )

            recexp_update = self.moco.ProjectRecurringExpense.update(
                project_id=project.id,
                recurring_expense_id=recexp_create.data.id,
                title=title,
                quantity=quantity,
                unit=unit,
                unit_price=unit_price,
                unit_cost=unit_cost,
                finish_date=finish_date,
                description=description,
                billable=billable,
                budget_relevant=budget_relevant,
            )

            assert recexp_create.response.status_code == 200
            assert recexp_update.response.status_code == 200

            assert type(recexp_create) is ObjectResponse
            assert type(recexp_update) is ObjectResponse

            assert recexp_update.data.start_date == start_date.isoformat()
            assert recexp_update.data.period == period
            assert recexp_update.data.quantity == quantity
            assert recexp_update.data.unit == unit
            assert recexp_update.data.unit_price == unit_price
            assert recexp_update.data.unit_cost == unit_cost
            assert recexp_update.data.finish_date == finish_date.isoformat()
            assert recexp_update.data.description == description
            assert recexp_update.data.billable == billable
            assert recexp_update.data.budget_relevant == budget_relevant

    def test_delete_finish_date(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectRecurringExpense.test_delete_finish_date"):
            finish_date = date(2021, 1, 1)

            recexp_create_with_finish = self.moco.ProjectRecurringExpense.create(
                project_id=project.id,
                start_date=date(2020, 1, 1),
                period=ProjectRecurringExpensePeriod.WEEKLY,
                title="TestProjectRecurringExpense.test_delete_finish_date_create",
                quantity=1,
                unit="h",
                unit_price=2,
                unit_cost=1,
                finish_date=finish_date
            )

            recexp_update_delete_finish = self.moco.ProjectRecurringExpense.update(
                project_id=project.id,
                recurring_expense_id=recexp_create_with_finish.data.id,
                finish_date=""
            )

            assert recexp_create_with_finish.response.status_code == 200
            assert recexp_update_delete_finish.response.status_code == 200

            assert type(recexp_create_with_finish) is ObjectResponse
            assert type(recexp_update_delete_finish) is ObjectResponse

            assert recexp_create_with_finish.data.finish_date == finish_date.isoformat()
            assert recexp_update_delete_finish.data.finish_date is None

    def test_get(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectRecurringExpense.test_get"):
            start_date = date(2020, 1, 1)
            period = ProjectRecurringExpensePeriod.BIWEEKLY
            title = "TestProjectRecurringExpense.test_get_create"
            quantity = 1.5
            unit = "h"
            unit_price = 32.5
            unit_cost = 20.5
            finish_date = date(2021, 1, 1)
            description = "dummy recurring expense, test get"
            billable = False
            budget_relevant = True

            recexp_create = self.moco.ProjectRecurringExpense.create(
                project_id=project.id,
                start_date=start_date,
                period=period,
                title=title,
                quantity=quantity,
                unit=unit,
                unit_price=unit_price,
                unit_cost=unit_cost,
                finish_date=finish_date,
                description=description,
                billable=billable,
                budget_relevant=budget_relevant,
            )

            recexp_get = self.moco.ProjectRecurringExpense.get(
                project_id=project.id,
                recurring_expense_id=recexp_create.data.id
            )

            assert recexp_create.response.status_code == 200
            assert recexp_get.response.status_code == 200

            assert type(recexp_create) is ObjectResponse
            assert type(recexp_get) is ObjectResponse

            assert recexp_get.data.start_date == start_date.isoformat()
            assert recexp_get.data.period == period
            assert recexp_get.data.quantity == quantity
            assert recexp_get.data.unit == unit
            assert recexp_get.data.unit_price == unit_price
            assert recexp_get.data.unit_cost == unit_cost
            assert recexp_get.data.finish_date == finish_date.isoformat()
            assert recexp_get.data.description == description
            assert recexp_get.data.billable == billable
            assert recexp_get.data.budget_relevant == budget_relevant

    def test_delete(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectRecurringExpense.test_delete"):
            recexp_create = self.moco.ProjectRecurringExpense.create(
                project_id=project.id,
                start_date=date(2020, 1, 1),
                period=ProjectRecurringExpensePeriod.WEEKLY,
                title="TestProjectRecurringExpense.test_delete_create",
                quantity=1,
                unit="h",
                unit_price=2,
                unit_cost=1,
            )

            recexp_delete = self.moco.ProjectRecurringExpense.delete(
                project_id=project.id,
                recurring_expense_id=recexp_create.data.id,
            )

            assert recexp_create.response.status_code == 200
            assert recexp_delete.response.status_code == 204

            assert type(recexp_delete) is EmptyResponse
