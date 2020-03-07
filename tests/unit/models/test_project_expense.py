import pytest
from .. import UnitTest

class TestProjectExpense(UnitTest):
    def test_create(self):
        project_id = 2
        date = '2019-10-10'
        title = "this is an expense"
        quantity = 3
        unit = "server"
        unit_price = 200
        unit_cost = 100
        description = "this is the description of the server that is in the expense"
        billable = False
        budget_relevant = True
        custom_properties = {
            "server_os" : "Windows XP"
        }

        response = self.moco.ProjectExpense.create(project_id, date, title, quantity, unit, unit_price, unit_cost, description=description, billable=billable, budget_relevant=budget_relevant, custom_properties=custom_properties)
        data = response["data"]

        assert data["date"] == date
        assert data["title"] == title
        assert data["quantity"] == quantity
        assert data["unit"] == unit
        assert data["unit_price"] == unit_price
        assert data["unit_cost"] == unit_cost
        assert data["description"] == description
        assert data["billable"] == billable
        assert data["budget_relevant"] == budget_relevant
        assert data["custom_properties"] == custom_properties

        assert response["method"] == "POST"

    def test_create_default_billable(self):
        billable_default = True

        project_id = 2
        date = '2019-10-10'
        title = "this is an expense"
        quantity = 3
        unit = "server"
        unit_price = 200
        unit_cost = 100

        response = self.moco.ProjectExpense.create(project_id, date, title, quantity, unit, unit_price, unit_cost)
        data = response["data"]

        assert data["billable"] == billable_default

    def test_create_default_budget_relevant(self):
        budget_relevant_default = False

        project_id = 2
        date = '2019-10-10'
        title = "this is an expense"
        quantity = 3
        unit = "server"
        unit_price = 200
        unit_cost = 100

        response = self.moco.ProjectExpense.create(project_id, date, title, quantity, unit, unit_price, unit_cost)
        data = response["data"]

        assert data["budget_relevant"] == budget_relevant_default


    def test_create_bulk(self):
        project_id = 2
        items = [
            {
                "date" : "2019-10-10",
                "title" : "more server hosting",
                "quanity": 4,
                "unit": "server",
                "unit_price": 400,
                "unit_cost" : 200
            },
            {

                "date" : "2011-03-04",
                "title" : "image hosting",
                "quanity": 45,
                "unit": "image",
                "unit_price": 3200,
                "unit_cost" : 300
            }
        ]

        response = self.moco.ProjectExpense.create_bulk(project_id, items)
        data = response["data"]

        assert data["bulk_data"] == items
        assert response["method"] == "POST"


    def test_update(self):
        expense_id = 1
        project_id = 2
        expense_date = '2019-10-10'
        title = "this is an expense"
        quantity = 3
        unit = "server"
        unit_price = 200
        unit_cost = 100
        description = "this is the description of the server that is in the expense"
        billable = False
        budget_relevant = True
        custom_properties = {
            "server_os" : "Windows XP"
        }

        response = self.moco.ProjectExpense.update(project_id, expense_id, expense_date=expense_date, title=title, quantity=quantity, unit=unit, unit_price=unit_price, unit_cost=unit_cost, description=description, billable=billable, budget_relevant=budget_relevant, custom_properties=custom_properties)
        data = response["data"]

        assert data["date"] == expense_date
        assert data["title"] == title
        assert data["quantity"] == quantity
        assert data["unit"] == unit
        assert data["unit_price"] == unit_price
        assert data["unit_cost"] == unit_cost
        assert data["description"] == description
        assert data["billable"] == billable
        assert data["budget_relevant"] == budget_relevant
        assert data["custom_properties"] == custom_properties

        assert response["method"] == "PUT"

    def test_delete(self):
        project_id = 2
        expense_id = 3

        response = self.moco.ProjectExpense.delete(project_id, expense_id)

        assert response["method"] == "DELETE"

    def test_disregard(self):
        project_id = 2
        expense_ids = [1,2,3,4]
        reason = "this is the reason for disgarding the expenses"

        response = self.moco.ProjectExpense.disregard(project_id, expense_ids, reason)
        data = response["data"]

        assert data["expense_ids"] == expense_ids
        assert data["reason"] == reason
        assert response["method"] == "POST"

    def test_getall(self):
        from_date = "2019-10-10"
        to_date = '2018-10-02'

        response = self.moco.ProjectExpense.getall(from_date=from_date, to_date=to_date)
        params = response["params"]

        assert params["from"] == from_date
        assert params["to"] == to_date
        assert response["method"] == "GET"

    def test_getall_sort_default(self):
        sort_by = "field to sort by"

        response = self.moco.ProjectExpense.getall(sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getall_sort_overwrite(self):
        sort_by = "field to sort by"
        sort_order = "desc"

        response = self.moco.ProjectExpense.getall(sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getall_page_default(self):
        page_default = 1

        response = self.moco.ProjectExpense.getall()
        assert response["params"]["page"] == page_default

    def test_getall_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.ProjectExpense.getall(page=page_overwrite)
        assert response["params"]["page"] == page_overwrite

    def test_get(self):
        project_id = 2
        expense_id = 4

        response = self.moco.ProjectExpense.get(project_id, expense_id)

        assert response["method"] == "GET"

    def test_getlist(self):
        project_id = 2

        response = self.moco.ProjectExpense.getlist(project_id)

        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        project_id = 2
        sort_by = "default field to sort by"

        response = self.moco.ProjectExpense.getlist(project_id, sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)


    def test_getlist_sort_overwrite(self):
        project_id = 2
        sort_by = "default field to sort by"
        sort_order = "desc"

        response = self.moco.ProjectExpense.getlist(project_id, sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)      

    def test_getlist_page_default(self):
        project_id = 1
        page_default = 1

        response = self.moco.ProjectExpense.getlist(project_id)
        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        project_id = 1
        page_overwrite = 22

        response = self.moco.ProjectExpense.getlist(project_id, page=page_overwrite)
        assert response["params"]["page"] == page_overwrite
        