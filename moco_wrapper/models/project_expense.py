from .base import MocoBase
from ..const import API_PATH

class ProjectExpense(MocoBase):
    """Class for handling additional project expenses.  """

    def __init__(self, moco):
        self._moco = moco

    def create(
        self,
        project_id,
        date,
        title,
        quantity,
        unit,
        unit_price,
        unit_cost,
        description = None,
        billable = True,
        budget_relevant = False,
        custom_properties = None
        ):
        """create an additional project expense

        :param project_id: id of the project to create the expense for
        :param date: date of the expense, format (YYYY-MM-DD)
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
            "date": date,
            "title" : title,
            "quantity": quantity,
            "unit" : unit,
            "unit_price": unit_price,
            "unit_cost" : unit_cost,
        }

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
        project_id,
        items,
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
        project_id,
        expense_id,
        date = None,
        title = None,
        quantity = None,
        unit = None,
        unit_price = None,
        unit_cost = None,
        description = None,
        billable = None,
        budget_relevant = None,
        custom_properties = None
        ):
        """update an existing additional project expsnse

        :param project_id: id of the project
        :param expense_id: id of the expense we want to update
        :param date: date of the expense, format (YYYY-MM-DD)
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
            ("date", date),
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
                data[key] = value

        print (API_PATH["project_expense_update"].format(project_id=project_id, expense_id=expense_id))

        return self._moco.put(API_PATH["project_expense_update"].format(project_id=project_id, expense_id=expense_id), data=data)

    def delete(
        self,
        project_id,
        expense_id
        ):
        """deletes an expense

        :param project_id: id of the project the expense belongs to
        :param expense_id: id of the expense to delete
        """

        return self._moco.delete(API_PATH["project_expense_delete"].format(project_id=project_id, expense_id=expense_id))

    def disregard(
        self,
        project_id,
        expense_ids,
        reason
        ):
        """mark expenses as "already billed"

        :param project_id: id of the project
        :param expense_ids: array of expense ids to mark as "already billed"
        :param reason: reason for disregarding the expenses
        """


        data = {
            "expense_ids" : expense_ids,
            "reason": reason
        }

        return self._moco.post(API_PATH["project_expense_disregard"].format(project_id=project_id), data=data)

    def getall(
        self,
        from_date = None,
        to_date = None,
        sort_by = None,
        sort_order = 'asc'
        ):
        """get a list of all additional expenses

        :param from_date: starting date, format (YYYY-MM-DD)
        :param to_date: end date, format (YYYY-MM-DD)
        :param sort_by: sort results by field
        :param sort_order: asc or desc
        :returns: list of expense objects
        """

        params = {}
        for key, value in (
            ("from", from_date),
            ("to", to_date)
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["project_expense_getall"], params=params)

    def get(
        self,
        project_id,
        expense_id
        ):
        """retrieve a single expense object

        :param project_id: id of the project
        :param expense_id: if of the expense to retrieve
        :returns: expense object
        """

        return self._moco.get(API_PATH["project_expense_get"].format(project_id=project_id, expense_id=expense_id))

    def getlist(
        self,
        project_id,
        sort_by = None,
        sort_order = 'asc'
        ):
        """retrieve all expenses of a project

        :param project_id: id of the project
        :param sort_by: sort results by field
        :param sort_order: asc or desc
        :returns: list of expense objects
        """

        params = {}
        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["project_expense_getlist"].format(project_id=project_id), params=params)