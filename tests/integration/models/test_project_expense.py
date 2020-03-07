from moco_wrapper.util.response import JsonResponse, ListingResponse, EmptyResponse
from moco_wrapper.util.generator import ProjectExpenseGenerator

from datetime import date
from .. import IntegrationTest

class TestProjectExpense(IntegrationTest):
    def get_user(self):
        with self.recorder.use_cassette("TestProjectExpense.get_user"):
            user = self.moco.User.getlist().items[0]
            return user

    def get_customer(self):
        with self.recorder.use_cassette("TestProjectExpense.get_customer"):
            customer_create = self.moco.Company.create(
                "TestProjectExpense",
                company_type="customer"
            )

            return customer_create.data

    def get_project(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProjectExpense.get_project"):
            project_create = self.moco.Project.create(
                "dummy project, test expense",
                "EUR",
                user.id,
                customer.id,
                finish_date = date(2020, 1, 1),
            )

            return project_create.data

    def test_create(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectExpense.test_create"):
            ex_date = date(2020, 1, 1)
            title = "fire hydrants"
            quantity = 3.5
            unit = "stk"
            unit_price = 30 #selling price
            unit_cost = 20 #buying price

            ex_create = self.moco.ProjectExpense.create(
                project.id,
                ex_date,
                title,
                quantity,
                unit,
                unit_price,
                unit_cost
            )

            assert ex_create.response.status_code == 200

            assert isinstance(ex_create, JsonResponse)

            assert ex_create.data.project.id == project.id
            assert ex_create.data.company.id == project.customer.id
            assert ex_create.data.date == ex_date.isoformat()
            assert ex_create.data.quantity == quantity
            assert ex_create.data.unit == unit
            assert ex_create.data.unit_price == unit_price
            assert ex_create.data.unit_cost == unit_cost

    def test_create_full(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectExpense.test_create_full"):
            ex_date = date(2020, 1, 1)
            title = "fire hydrants"
            quantity = 3.5
            unit = "stk"
            unit_price = 30 #selling price
            unit_cost = 20 #buying price
            description = "misc tools"
            billable = True
            budget_relevant = True

            ex_create = self.moco.ProjectExpense.create(
                project.id,
                ex_date,
                title,
                quantity,
                unit,
                unit_price,
                unit_cost,
                description=description,
                billable=billable,
                budget_relevant=budget_relevant
            )

            assert ex_create.response.status_code == 200

            assert isinstance(ex_create, JsonResponse)

            assert ex_create.data.project.id == project.id
            assert ex_create.data.company.id == project.customer.id
            assert ex_create.data.date == ex_date.isoformat()
            assert ex_create.data.quantity == quantity
            assert ex_create.data.unit == unit
            assert ex_create.data.unit_price == unit_price
            assert ex_create.data.unit_cost == unit_cost
            assert ex_create.data.description == description
            assert ex_create.data.billable == billable
            assert ex_create.data.budget_relevant == budget_relevant

    def test_get(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectExpense.test_get"):
            ex_date = date(2020, 1, 1)
            title = "fire hydrants"
            quantity = 3.5
            unit = "stk"
            unit_price = 30 #selling price
            unit_cost = 20 #buying price
            description = "misc tools"
            billable = True
            budget_relevant = True

            ex_create = self.moco.ProjectExpense.create(
                project.id,
                ex_date,
                title,
                quantity,
                unit,
                unit_price,
                unit_cost,
                description=description,
                billable=billable,
                budget_relevant=budget_relevant
            )

            ex_get = self.moco.ProjectExpense.get(project.id, ex_create.data.id)

            assert ex_create.response.status_code == 200
            assert ex_get.response.status_code == 200

            assert isinstance(ex_create, JsonResponse)
            assert isinstance(ex_get, JsonResponse)

            assert ex_get.data.project.id == project.id
            assert ex_get.data.company.id == project.customer.id
            assert ex_get.data.date == ex_date.isoformat()
            assert ex_get.data.quantity == quantity
            assert ex_get.data.unit == unit
            assert ex_get.data.unit_price == unit_price
            assert ex_get.data.unit_cost == unit_cost
            assert ex_get.data.description == description
            assert ex_get.data.billable == billable
            assert ex_get.data.budget_relevant == budget_relevant

    def test_update(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectExpense.test_update"):
            ex_date = date(2020, 1, 1)
            title = "fire hydrants"
            quantity = 3.5
            unit = "stk"
            unit_price = 30 #selling price
            unit_cost = 20 #buying price
            description = "misc tools"
            billable = True
            budget_relevant = True

            ex_create = self.moco.ProjectExpense.create(
                project.id,
                date(2004, 1, 1),
                "dummy expense, text update",
                1,
                "h",
                2,
                3
            )

            ex_update = self.moco.ProjectExpense.update(
                project.id,
                ex_create.data.id,
                expense_date=ex_date,
                title=title,
                quantity=quantity,
                unit=unit,
                unit_price=unit_price,
                unit_cost=unit_cost,
                description=description,
                billable=billable,
                budget_relevant=budget_relevant
            )

            assert ex_create.response.status_code == 200
            assert ex_update.response.status_code == 200

            assert isinstance(ex_create, JsonResponse)
            assert isinstance(ex_update, JsonResponse)

            assert ex_update.data.project.id == project.id
            assert ex_update.data.company.id == project.customer.id
            assert ex_update.data.date == ex_date.isoformat()
            assert ex_update.data.quantity == quantity
            assert ex_update.data.unit == unit
            assert ex_update.data.unit_price == unit_price
            assert ex_update.data.unit_cost == unit_cost
            assert ex_update.data.description == description
            assert ex_update.data.billable == billable
            assert ex_update.data.budget_relevant == budget_relevant

    def test_delete(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectExpense.test_delete"):
            ex_create = self.moco.ProjectExpense.create(
                project.id,
                date(2020, 1, 1),
                "dummy expnese, test delete",
                1,
                "h",
                2,
                3
            )

            ex_delete = self.moco.ProjectExpense.delete(project.id, ex_create.data.id)
            
            assert ex_create.response.status_code == 200
            assert ex_delete.response.status_code == 204

            assert isinstance(ex_create, JsonResponse)
            assert isinstance(ex_delete, EmptyResponse)

    def test_getlist(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectExpense.test_getlist"):
            ex_list = self.moco.ProjectExpense.getlist(project.id)

            assert ex_list.response.status_code == 200
            
            assert isinstance(ex_list, ListingResponse)

            assert ex_list.current_page == 1
            assert ex_list.is_last is not None
            assert ex_list.next_page is not None
            assert ex_list.total is not None
            assert ex_list.page_size is not None

    def test_getall(self):
        with self.recorder.use_cassette("TestProjectExpense.test_getall"):
            ex_list = self.moco.ProjectExpense.getall(
                from_date=date(2020, 1, 1),
                to_date=date(2021, 1, 1)
            )

            assert ex_list.response.status_code == 200
            
            assert isinstance(ex_list, ListingResponse)

            assert ex_list.current_page == 1
            assert ex_list.is_last is not None
            assert ex_list.next_page is not None
            assert ex_list.total is not None
            assert ex_list.page_size is not None

    def test_create_bulk(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectExpense.test_create_bulk"):
            gen = ProjectExpenseGenerator()
            
            items = [
                gen.generate(
                    date(2020, 1, 1),
                    "dummy project expense, test create bulk (1)",
                    1,
                    "stk",
                    2,
                    3,
                ),
                gen.generate(
                    date(2021, 1, 1),
                    "dummy project expense, test create bulk (2)",
                    1,
                    "stk",
                    2,
                    3,
                )
            ]

            ex_bulk = self.moco.ProjectExpense.create_bulk(project.id, items)

            assert ex_bulk.response.status_code == 200

            assert isinstance(ex_bulk, ListingResponse)

            assert ex_bulk.current_page == 1
            assert ex_bulk.is_last is not None
            assert ex_bulk.next_page is not None
            assert ex_bulk.total is not None
            assert ex_bulk.page_size is not None

    def test_disregard_items(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectExpense.test_disregard"):
            gen = ProjectExpenseGenerator()

            items = [
                gen.generate(
                    date(2020, 1, 1),
                    "dummy project expense, test create bulk (1)",
                    1,
                    "stk",
                    2,
                    3,
                ),
                gen.generate(
                    date(2021, 1, 1),
                    "dummy project expense, test create bulk (2)",
                    1,
                    "stk",
                    2,
                    3,
                )
            ]

            ex_bulk = self.moco.ProjectExpense.create_bulk(
                project.id,
                items
            )
            
            disregard_expense_ids = [x.id for x in ex_bulk.items]
            ex_disregard = self.moco.ProjectExpense.disregard(
                project.id,
                disregard_expense_ids,
                "disregard dummy expenses"
            )

            assert ex_bulk.response.status_code == 200
            assert ex_disregard.response.status_code == 204

            assert isinstance(ex_bulk, ListingResponse)
            assert isinstance(ex_disregard, EmptyResponse)

            assert ex_bulk.current_page == 1
            assert ex_bulk.is_last is not None
            assert ex_bulk.next_page is not None
            assert ex_bulk.total is not None
            assert ex_bulk.page_size is not None
            