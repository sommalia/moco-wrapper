from ..const import API_PATH
from .base import MocoBase

class ProjectRecurringExpense(MocoBase):
    """class for handling recurring expenses of a project."""

    def __init__(self, moco):
        self._moco = moco

    def getlist(
        self,
        project_id,
        sort_by = None,
        sort_order = 'asc'
        ):
        """retrieve a list of recurring expenses on a project

        :param project_id: id of the project the expesen belongs to
        :param sort_by: field to sort results by
        :param sort_order: asc or desc
        :returns: list of recurring expenses
        """
        pass

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
        pass

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
        billable = None,
        budget_relevant = None,
        custom_properties = None,
        ):
        pass

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
        pass

    def delete(
        self,
        project_id,
        recurring_expense_id,
        ):
        pass
