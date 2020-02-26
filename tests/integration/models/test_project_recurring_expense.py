from moco_wrapper.util.response import ListingResponse, JsonResponse, EmptyResponse
from moco_wrapper.models.project_recurring_expense import ProjectRecurringExpensePeriod

from datetime import date
from .. import IntegrationTest

class TestProjectRecurringExpense(IntegrationTest):
    def get_customer(self):
        with self.recorder.use_cassette("TestProjectRecurringExpense.get_customer"):
            customer_create = self.moco.Company.create(
                "TestProjectRecurringExpense",
                company_type="customer"
            )

            return customer_create.data
    
    def get_user(self):
        with self.recorder.use_cassette("TestProjectRecurringExpense.get_user"):
            user = self.moco.User.getlist().items[0]
            return user
    
    def get_project(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProjectRecurringExpense.get_project"):
            project_create = self.moco.Project.create(
                "dummy project, test recurring expense",
                "EUR",
                user.id,
                customer.id,
                finish_date = date(2020, 1, 1)
            )

            return project_create.data

    def test_getlist(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectRecurringExpense.test_getlist"):
            recexp_list = self.moco.ProjectRecurringExpense.getlist(project.id)

            assert recexp_list.response.status_code == 200
            
            assert isinstance(recexp_list, ListingResponse)

    def test_create(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectRecurringExpense.test_create"):
            start_date = date(2020, 1, 1)
            period = ProjectRecurringExpensePeriod.BIWEEKLY
            title = "hosting xs - special support"
            quantity = 1.5
            unit = "h"
            unit_price = 32.5
            unit_cost = 20.5

            recexp_create = self.moco.ProjectRecurringExpense.create(
                project.id,
                start_date,
                period,
                title,
                quantity,
                unit,
                unit_price,
                unit_cost,
            )

            assert recexp_create.response.status_code == 200

            assert isinstance(recexp_create, JsonResponse)

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
            title = "hosting xs - special support"
            quantity = 1.5
            unit = "h"
            unit_price = 32.5
            unit_cost = 20.5
            finish_date = date(2021, 1, 1)
            description = "dummy recurring expense, test create full"
            billable = False
            budget_relevant = True


            recexp_create = self.moco.ProjectRecurringExpense.create(
                project.id,
                start_date,
                period,
                title,
                quantity,
                unit,
                unit_price,
                unit_cost,
                finish_date=finish_date,
                description=description,
                billable=billable,
                budget_relevant=budget_relevant,
            )

            assert recexp_create.response.status_code == 200

            assert isinstance(recexp_create, JsonResponse)

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
            title = "hosting xs - special support"
            quantity = 1.5
            unit = "h"
            unit_price = 32.5
            unit_cost = 20.5
            finish_date = date(2021, 1, 1)
            description = "dummy recurring expense, test update"
            billable = False
            budget_relevant = True

            recexp_create = self.moco.ProjectRecurringExpense.create(
                project.id,
                start_date,
                period,
                "dummy recurring expense, test update",
                1,
                "h",
                2,
                1
            )

            recexp_update = self.moco.ProjectRecurringExpense.update(
                project.id,
                recexp_create.data.id,
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

            assert isinstance(recexp_create, JsonResponse)
            assert isinstance(recexp_update, JsonResponse)

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
                project.id,
                date(2020, 1, 1),
                ProjectRecurringExpensePeriod.WEEKLY,
                "dummy recurring expense, test delete finish date",
                1,
                "h",
                2,
                1,
                finish_date=finish_date
            )

            recexp_update_delete_finish = self.moco.ProjectRecurringExpense.update(
                project.id,
                recexp_create_with_finish.data.id,
                finish_date=""
            )

            assert recexp_create_with_finish.response.status_code == 200
            assert recexp_update_delete_finish.response.status_code == 200

            assert isinstance(recexp_create_with_finish, JsonResponse)
            assert isinstance(recexp_update_delete_finish, JsonResponse)

            assert recexp_create_with_finish.data.finish_date == finish_date.isoformat()
            assert recexp_update_delete_finish.data.finish_date == None
    
    def test_get(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectRecurringExpense.test_get"):
            start_date = date(2020, 1, 1)
            period = ProjectRecurringExpensePeriod.BIWEEKLY
            title = "hosting xs - special support"
            quantity = 1.5
            unit = "h"
            unit_price = 32.5
            unit_cost = 20.5
            finish_date = date(2021, 1, 1)
            description = "dummy recurring expense, test get"
            billable = False
            budget_relevant = True


            recexp_create = self.moco.ProjectRecurringExpense.create(
                project.id,
                start_date,
                period,
                title,
                quantity,
                unit,
                unit_price,
                unit_cost,
                finish_date=finish_date,
                description=description,
                billable=billable,
                budget_relevant=budget_relevant,
            )

            recexp_get = self.moco.ProjectRecurringExpense.get(
                project.id,
                recexp_create.data.id
            )

            assert recexp_create.response.status_code == 200
            assert recexp_get.response.status_code == 200

            assert isinstance(recexp_create, JsonResponse)
            assert isinstance(recexp_get, JsonResponse)

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
                project.id,
                date(2020, 1, 1),
                ProjectRecurringExpensePeriod.WEEKLY,
                "dummy recurring expense, test delete",
                1,
                "h",
                2,
                1,
            )

            recexp_delete = self.moco.ProjectRecurringExpense.delete(
                project.id,
                recexp_create.data.id,
            )

            assert recexp_create.response.status_code == 200
            assert recexp_delete.response.status_code == 204

            assert isinstance(recexp_delete, EmptyResponse)