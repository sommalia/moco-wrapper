from .base import MWRAPBase
from ..const import API_PATH

class ProjectRecurringExpense(MWRAPBase):
    """class for handling recurring expenses of a project."""

    def __init__(self, moco):
        self._moco = moco

    def getlist(
        self,
        project_id,
        sort_by = None,
        sort_order = 'asc',
        page = 1
        ):
        """retrieve a list of recurring expenses on a project

        :param project_id: id of the project the expesen belongs to
        :param sort_by: field to sort results by
        :param sort_order: asc or desc (default asc)
        :param page: page number (default 1)
        :returns: list of recurring expenses
        """
        params = {}

        for key, value in (
            ("page", page),
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["project_recurring_expense_getlist"].format(project_id=project_id), params=params)

    def get(
        self,
        project_id,
        recurring_expense_id,
        ):
        """retrieve a single recurring expense

        :param project_id: id of the project the expesen belongs to
        :param recurring_expense_id: id of the recurring expense
        :returns: a single recurring expense object
        """
        return self._moco.get(API_PATH["project_recurring_expense_get"].format(project_id=project_id, recurring_expense_id=recurring_expense_id))

    def create(
        self,
        project_id,
        start_date,
        period,
        title, 
        quantity,
        unit,
        unit_price,
        unit_cost,
        finish_date = None,
        description = None,
        billable = True,
        budget_relevant = False,
        custom_properties = None,
        ):
        """create a new recurring expense on a project

        :param project_id: id of the project to create the expense for
        :param start_date: starting date of the expense (format YYYY-MM-DD)
        :param period: period of the expense ("weekly", "biweekly", "monthly", "quarterly", "biannual" or "annual")
        :param title: title of the expense
        :param quantity: quantity (ex. 5)
        :param unit: unit name (ex. "Server")
        :param unit_price: unit price (ex. 400.50)
        :param unit_cost: unit cost (ex. 320.13)
        :param finish_date: finish date (format YYYY-MM-DD) (if empty: unlimited)
        :param description: description text
        :param billable: true/false billable or not (default true)
        :param budget_relevant: true/false budget relevant or not (default false)
        :param custom_properties: custom fields to add
        :returns: the created recurring expense object
        """
        data = {
            "start_date": start_date,
            "period": period,
            "title": title,
            "quantity": quantity,
            "unit": unit,
            "unit_price": unit_price,
            "unit_cost": unit_cost
        }

        for key, value in (
            ("finish_date", finish_date),
            ("description", description),
            ("billable", billable),
            ("budget_relevant", budget_relevant),
            ("custom_properties", custom_properties)
        ):
            if value is not None:
                data[key] = value

        return self._moco.post(API_PATH["project_recurring_expense_create"].format(project_id=project_id), data=data)

    def update(
        self,
        project_id,
        recurring_expense_id,
        title = None, 
        quantity = None,
        unit = None,
        unit_price = None,
        unit_cost = None,
        finish_date = None,
        description = None,
        billable = None,
        budget_relevant = None,
        custom_properties = None,
        ):
        """update an existing recurring expense

        :param project_id: id of the project
        :param recurring_expense_id: id of the expense to update
        :param title: title of the expense
        :param quantity: quantity (ex. 5)
        :param unit: unit name (ex. "Server")
        :param unit_price: unit price (ex. 400.50)
        :param unit_cost: unit cost (ex. 320.13)
        :param finish_date: finish date (format YYYY-MM-DD) (if empty: unlimited)
        :param description: description text
        :param billable: true/false billable or not
        :param budget_relevant: true/false budget relevant or not
        :param custom_properties: custom fields to add
        :returns: the updated recurring expense object
        """
        data = {}
        for key, value in (
            ("title", title),
            ("quantity", quantity),
            ("unit", unit),
            ("unit_price", unit_price),
            ("unit_cost", unit_cost),
            ("finish_date", finish_date),
            ("description", description),
            ("billable", billable),
            ("budget_relevant", budget_relevant),
            ("custom_properties", custom_properties)
        ):
            if value is not None:
                data[key] = value

        return self._moco.put(API_PATH["project_recurring_expense_update"].format(project_id=project_id, recurring_expense_id=recurring_expense_id), data=data)

    def delete(
        self,
        project_id,
        recurring_expense_id,
        ):
        """deletes an existing expense

        :param project_id: project id the expense belongs to
        :param recurring_expense_id: id of the expense to delete
        """
        return self._moco.delete(API_PATH["project_recurring_expense_delete"].format(project_id=project_id, recurring_expense_id=recurring_expense_id))
