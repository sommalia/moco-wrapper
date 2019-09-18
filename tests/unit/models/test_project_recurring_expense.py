from .. import UnitTest
import pytest

class TestProjectRecurringExpense(UnitTest):
    def test_getlist(self):
        project_id = 2

        response = self.moco.ProjectRecurringExpense.getlist(project_id)

        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        project_id = 2
        sort_by = "field to sort by"

        response = self.moco.ProjectRecurringExpense.getlist(project_id, sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        project_id = 2
        sort_by = "field to sort by"
        sort_order = "desc"

        response = self.moco.ProjectRecurringExpense.getlist(project_id, sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        project_id = 1
        page_default = 1

        response = self.moco.ProjectRecurringExpense.getlist(project_id)
        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        project_id = 1
        page_overwrite = 22

        response = self.moco.ProjectRecurringExpense.getlist(project_id, page=page_overwrite)
        assert response["params"]["page"] == page_overwrite

    def test_get(self):
        project_id = 2
        expense_id = 400

        response = self.moco.ProjectRecurringExpense.get(project_id, expense_id)

        assert response["method"] == "GET"

    def test_create(self):
        project_id = 2
        start_date = '2019-10-10'
        period = "weekly"
        title = "hosting xl"
        quantity = 100
        unit = "vserver"
        unit_price = 20
        unit_cost = 13.5
        
        finish_date = '2020-10-10'
        description = "this is a note"
        billable = False
        budget_relevant = True
        custom_properties = {
            "add_dog": True
        }

        response = self.moco.ProjectRecurringExpense.create(project_id, start_date, period, title, quantity, unit, unit_price, unit_cost, finish_date=finish_date, description=description, billable=billable, budget_relevant=budget_relevant, custom_properties=custom_properties)
        data = response["data"]

        assert data["start_date"] == start_date
        assert data["period"] == period
        assert data["title"] == title
        assert data["quantity"] == quantity
        assert data["unit"] == unit
        assert data["unit_price"] == unit_price
        assert data["unit_cost"] == unit_cost
        assert data["finish_date"] == finish_date
        assert data["description"] == description
        assert data["billable"] == billable
        assert data["budget_relevant"] == budget_relevant
        assert data["custom_properties"] == custom_properties

        assert response["method"] == "POST"

    def test_create_default_billable(self):
        project_id = 2
        start_date = '2019-10-10'
        period = "weekly"
        title = "hosting xl"
        quantity = 100
        unit = "vserver"
        unit_price = 20
        unit_cost = 13.5

        billable_default = True

        response = self.moco.ProjectRecurringExpense.create(project_id, start_date, period, title, quantity, unit, unit_price, unit_cost)
        data = response["data"]

        assert data["billable"] == billable_default

    def test_create_default_budget_relevant(self):
        project_id = 2
        start_date = '2019-10-10'
        period = "weekly"
        title = "hosting xl"
        quantity = 100
        unit = "vserver"
        unit_price = 20
        unit_cost = 13.5

        budget_relevant_default = False

        response = self.moco.ProjectRecurringExpense.create(project_id, start_date, period, title, quantity, unit, unit_price, unit_cost)
        data = response["data"]

        assert data["budget_relevant"] == budget_relevant_default


    def test_update(self):
        project_id = 2
        expense_id = 123
        start_date = '2019-10-10'
        period = "weekly"
        title = "hosting xl"
        quantity = 100
        unit = "vserver"
        unit_price = 20
        unit_cost = 13.5
        
        finish_date = '2020-10-10'
        description = "this is a note"
        billable = False
        budget_relevant = True
        custom_properties = {
            "add_dog": True
        }

        response = self.moco.ProjectRecurringExpense.update(project_id, expense_id, title=title, quantity=quantity, unit=unit, unit_price=unit_price, unit_cost=unit_cost, finish_date=finish_date, description=description, billable=billable, budget_relevant=budget_relevant, custom_properties=custom_properties)
        data = response["data"]

        assert data["title"] == title
        assert data["quantity"] == quantity
        assert data["unit"] == unit
        assert data["unit_price"] == unit_price
        assert data["unit_cost"] == unit_cost
        assert data["finish_date"] == finish_date
        assert data["description"] == description
        assert data["billable"] == billable
        assert data["budget_relevant"] == budget_relevant
        assert data["custom_properties"] == custom_properties

        assert response["method"] == "PUT"

    def test_delete(self):
        project_id = 2
        expense_id = 123

        response = self.moco.ProjectRecurringExpense.delete(project_id, expense_id)

        assert response["method"] == "DELETE"