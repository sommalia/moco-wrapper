from datetime import date

from .base import MWRAPBase
from ..const import API_PATH

class ProjectExpense(MWRAPBase):
    """Class for handling additional project expenses.  """

    def __init__(self, moco):
        self._moco = moco

    def create(
        self,
        project_id: int,
        expense_date: date,
        title: str,
        quantity: float,
        unit: str,
        unit_price: float,
        unit_cost: float,
        description: str = None,
        billable: bool = True,
        budget_relevant: bool = False,
        custom_properties: dict = None
        ):
        """create an additional project expense

        :param project_id: id of the project to create the expense for
        :param expense_date: date of the expense
        :param title: title string of the expense
        :param quantity: quantity 
        :param unit: name of the unit that is sold
        :param unit_price: price of the unit that is sold
        :param unit_cost: const of the unit that is sold
        :param description: descripion of the expense
        :param billable: true/false is this expense billable, yes or no? (default true)
        :param budget_relevant: true/false is this expense relevant for the budget of the project? (default false)
        :param custom_properties: additional fields as dictionary
        :returns: the created expense object

        """ 

        data = {
            "date": expense_date,
            "title" : title,
            "quantity": quantity,
            "unit" : unit,
            "unit_price": unit_price,
            "unit_cost" : unit_cost,
        }

        if isinstance(expense_date, date):
            data["date"] = expense_date.isoformat()

        for key, value in (
            ("description", description),
            ("billable", billable),
            ("budget_relevant", budget_relevant),
            ("custom_properties", custom_properties),
        ):
            if value is not None:
                data[key] = value

        return self._moco.post(API_PATH["project_expense_create"].format(project_id=project_id), data=data)

    def create_bulk(
        self,
        project_id: int,
        items: list,
        ):
        """create an multiple expenses for a project

        :param project_id: id of the project to created the expnses for
        :param items: bulk expense entries to create. A single entry consists of the same fields that are used when only creating one entry (also see PaymentExpenseGenerator)
        :returns: the created entries
        """
        
        data = {
            "bulk_data" : items
        }
        

        return self._moco.post(API_PATH["project_expense_create_bulk"].format(project_id=project_id), data=data)

    def update(
        self,
        project_id: int,
        expense_id: int,
        expense_date: date = None,
        title: str = None,
        quantity: float = None,
        unit: str = None,
        unit_price: float = None,
        unit_cost: float = None,
        description: str = None,
        billable: bool = None,
        budget_relevant: bool = None,
        custom_properties: dict = None
        ):
        """update an existing additional project expsnse

        :param project_id: id of the project
        :param expense_id: id of the expense we want to update
        :param expense_date: date of the expense
        :param title: title string of the expense
        :param quantity: quantity 
        :param unit: name of the unit that is sold
        :param unit_price: price of the unit that is sold
        :param unit_cost: const of the unit that is sold
        :param description: descripion of the expense
        :param billable: true/false is this expense billable, yes or no?
        :param budget_relevant: true/false is this expense relevant for the budget of the project?
        :param custom_properties: additional fields as dictionary
        :returns: the updated expense object
        """

        data = {}
        for key, value in (
            ("date", expense_date),
            ("title", title),
            ("quantity", quantity),
            ("unit", unit),
            ("unit_price", unit_price),
            ("unit_cost", unit_cost),
            ("description", description),
            ("billable", billable),
            ("budget_relevant", budget_relevant),
            ("custom_properties", custom_properties)
        ):
            if value is not None:
                if key in ["date"] and isinstance(value, date):
                    data[key] = value.isoformat()
                else:
                    data[key] = value

        print (API_PATH["project_expense_update"].format(project_id=project_id, expense_id=expense_id))

        return self._moco.put(API_PATH["project_expense_update"].format(project_id=project_id, expense_id=expense_id), data=data)

    def delete(
        self,
        project_id: int,
        expense_id: int
        ):
        """deletes an expense

        :param project_id: id of the project the expense belongs to
        :param expense_id: id of the expense to delete
        """

        return self._moco.delete(API_PATH["project_expense_delete"].format(project_id=project_id, expense_id=expense_id))

    def disregard(
        self,
        project_id: int,
        expense_ids: list,
        reason: str
        ):
        """disregard expeses

        :param project_id: id of the project
        :param expense_ids: array of expense ids to disregard
        :param reason: reason for disregarding the expenses
        :returns: empty response on success
        """


        data = {
            "expense_ids" : expense_ids,
            "reason": reason
        }

        return self._moco.post(API_PATH["project_expense_disregard"].format(project_id=project_id), data=data)

    def getall(
        self,
        from_date: date = None,
        to_date: date= None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
        ):
        """get a list of all additional expenses

        :param from_date: starting date, format (YYYY-MM-DD)
        :param to_date: end date, format (YYYY-MM-DD)
        :param sort_by: sort results by field
        :param sort_order: asc or desc (default asc)
        :param page: page number (default 1)
        :returns: list of expense objects
        """

        params = {}
        for key, value in (
            ("from", from_date),
            ("to", to_date),
            ("page", page),
        ):
            if value is not None:
                if key in ["from_date", "to_date"] and isinstance(value, date):
                    params[key] = value.isoformat()
                else:
                    params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["project_expense_getall"], params=params)

    def get(
        self,
        project_id: int,
        expense_id: int
        ):
        """retrieve a single expense object

        :param project_id: id of the project
        :param expense_id: if of the expense to retrieve
        :returns: expense object
        """

        return self._moco.get(API_PATH["project_expense_get"].format(project_id=project_id, expense_id=expense_id))

    def getlist(
        self,
        project_id: int,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
        ):
        """retrieve all expenses of a project

        :param project_id: id of the project
        :param sort_by: sort results by field
        :param sort_order: asc or desc (default asc)
        :param page: page number (default 1)
        :returns: list of expense objects
        """

        params = {}

        for key, value in (
            ("page", page),
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["project_expense_getlist"].format(project_id=project_id), params=params)