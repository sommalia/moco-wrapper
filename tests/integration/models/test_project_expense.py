from moco_wrapper.util.response import ObjectResponse, ListResponse, PagedListResponse, EmptyResponse
from moco_wrapper.util.generator import ProjectExpenseGenerator
from moco_wrapper.models.company import CompanyType

from datetime import date
from .. import IntegrationTest


class TestProjectExpense(IntegrationTest):
    def get_user(self):
        with self.recorder.use_cassette("TestProjectExpense.get_user"):
            user = self.moco.User.getlist()[0]
            return user

    def get_customer(self):
        with self.recorder.use_cassette("TestProjectExpense.get_customer"):
            customer_create = self.moco.Company.create(
                name="TestProjectExpense.get_customer",
                company_type=CompanyType.CUSTOMER
            )

            return customer_create.data

    def get_project(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProjectExpense.get_project"):
            project_create = self.moco.Project.create(
                name="TestProjectExpense.get_project",
                currency="EUR",
                leader_id=user.id,
                customer_id=customer.id,
                finish_date=date(2020, 1, 1),
            )

            return project_create.data

    def test_create(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectExpense.test_create"):
            ex_date = date(2020, 1, 1)
            title = "TestProjectExpense.test_create"
            quantity = 3.5
            unit = "stk"
            unit_price = 30  # selling price
            unit_cost = 20  # buying price

            ex_create = self.moco.ProjectExpense.create(
                project_id=project.id,
                expense_date=ex_date,
                title=title,
                quantity=quantity,
                unit=unit,
                unit_price=unit_price,
                unit_cost=unit_cost
            )

            assert ex_create.response.status_code == 200

            assert type(ex_create) is ObjectResponse

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
            title = "TestProjectExpense.test_create_full"
            quantity = 3.5
            unit = "stk"
            unit_price = 30  # selling price
            unit_cost = 20  # buying price
            description = "misc tools"
            billable = True
            budget_relevant = True

            ex_create = self.moco.ProjectExpense.create(
                project_id=project.id,
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

            assert type(ex_create) is ObjectResponse

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
            title = "TestProjectExpense.test_get_create"
            quantity = 3.5
            unit = "stk"
            unit_price = 30  # selling price
            unit_cost = 20  # buying price
            description = "misc tools"
            billable = True
            budget_relevant = True

            ex_create = self.moco.ProjectExpense.create(
                project_id=project.id,
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

            ex_get = self.moco.ProjectExpense.get(
                project_id=project.id,
                expense_id=ex_create.data.id
            )

            assert ex_create.response.status_code == 200
            assert ex_get.response.status_code == 200

            assert type(ex_create) is ObjectResponse
            assert type(ex_get) is ObjectResponse

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
            title = "TestProjectExpense.test_update"
            quantity = 3.5
            unit = "stk"
            unit_price = 30  # selling price
            unit_cost = 20  # buying price
            description = "misc tools"
            billable = True
            budget_relevant = True

            ex_create = self.moco.ProjectExpense.create(
                project_id=project.id,
                expense_date=date(2004, 1, 1),
                title="TestProjectExpense.test_update_create",
                quantity=1,
                unit="h",
                unit_price=2,
                unit_cost=3
            )

            ex_update = self.moco.ProjectExpense.update(
                project_id=project.id,
                expense_id=ex_create.data.id,
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

            assert type(ex_create) is ObjectResponse
            assert type(ex_update) is ObjectResponse

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
                project_id=project.id,
                expense_date=date(2020, 1, 1),
                title="TestProjectExpense.test_delete_create",
                quantity=1,
                unit="h",
                unit_price=2,
                unit_cost=3
            )

            ex_delete = self.moco.ProjectExpense.delete(
                project_id=project.id,
                expense_id=ex_create.data.id
            )

            assert ex_create.response.status_code == 200
            assert ex_delete.response.status_code == 204

            assert type(ex_create) is ObjectResponse
            assert type(ex_delete) is EmptyResponse

    def test_getlist(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectExpense.test_getlist"):
            ex_list = self.moco.ProjectExpense.getlist(
                project_id=project.id
            )

            assert ex_list.response.status_code == 200

            assert type(ex_list) is PagedListResponse

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

            assert type(ex_list) is PagedListResponse

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
                    expense_date=date(2020, 1, 1),
                    title="TestProjectExpense.test_create_bulk_create_1",
                    quantity=1,
                    unit="stk",
                    unit_price=2,
                    unit_cost=3,
                ),
                gen.generate(
                    expense_date=date(2021, 1, 1),
                    title="TestProjectExpense.test_create_bulk_create_2",
                    quantity=1,
                    unit="stk",
                    unit_price=2,
                    unit_cost=3,
                )
            ]

            ex_bulk = self.moco.ProjectExpense.create_bulk(
                project_id=project.id,
                items=items
            )

            assert ex_bulk.response.status_code == 200

            assert type(ex_bulk) is ListResponse

    def test_disregard_items(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectExpense.test_disregard"):
            gen = ProjectExpenseGenerator()

            items = [
                gen.generate(
                    expense_date=date(2020, 1, 1),
                    title="TestProjectExpense.test_create_bulk_create_1",
                    quantity=1,
                    unit="stk",
                    unit_price=2,
                    unit_cost=3,
                ),
                gen.generate(
                    expense_date=date(2021, 1, 1),
                    title="TestProjectExpense.test_create_bulk_create_2",
                    quantity=1,
                    unit="stk",
                    unit_price=2,
                    unit_cost=3,
                )
            ]

            ex_bulk = self.moco.ProjectExpense.create_bulk(
                project_id=project.id,
                items=items
            )

            disregard_expense_ids = [x.id for x in ex_bulk.items]
            ex_disregard = self.moco.ProjectExpense.disregard(
                project_id=project.id,
                expense_ids=disregard_expense_ids,
                reason="disregard dummy expenses"
            )

            assert ex_bulk.response.status_code == 200
            assert ex_disregard.response.status_code == 204

            assert type(ex_bulk) is ListResponse
            assert type(ex_disregard) is EmptyResponse

