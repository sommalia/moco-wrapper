import datetime

from .base import BaseGenerator


class ProjectExpenseGenerator(BaseGenerator):

    def generate(
        self,
        expense_date: datetime.date,
        title: str,
        quantity: float,
        unit: str,
        unit_price: float,
        unit_cost: float,
        description: str = None,
        billable: bool = True,
        budget_relevant: bool = False
    ) -> dict:
        """
        Create an item that can be used for creating bulk project expenses.

        :param project_id: Id of the project to create the expense for
        :param expense_date: Date of the expense
        :param title: Exense title
        :param quantity: Quantity (how much of ``unit`` was bought?)
        :param unit: Name of the unit (What was bought for the customer/project?)
        :param unit_price: Price of the unit that will be billed to the customer/project
        :param unit_cost: Cost that we had to pay
        :param description: Descripion of the expens
        :param billable: If this expense billable (default True)
        :param budget_relevant: If this expense is budget relevant (default False)

        :type project_id: int
        :type expense_date: datetime.date, str
        :type title: str
        :type quantity: float
        :type unit: str
        :type unit_price: float
        :type unit_cost: float
        :type description: str
        :type billable: bool
        :type budget_relevant: bool

        :returns: The created expense object

        Example usage:

        .. code-block:: python

            from moco_wrapper.util.generator import ProjectExpenseGenerator
            from moco_wrapper import Moco
            from datetime import date

            m = Moco()
            gen = ProjectExpenseGenerator()

            items = [
                gen.generate(
                    '2019-10-10',
                    "the title",
                    5,
                    "the unit",
                    20,
                    10
                ),
                gen.generate(
                    '2019-10-10',
                    "different title",
                    5,
                    "another unit",
                    20,
                    10,
                    billable=False,
                    description="the desc",
                    budget_relevant=True
                ),
                gen.generate(
                    date(2019, 10, 10),
                    "another title",
                    2,
                    "the unit",
                    20,
                    10
                ),
            ]
            project_id = 2

            created_expenses = m.ProjectExpense.create_bulk(project_id,items)

        .. seealso::

            :meth:`moco_wrapper.models.ProjectExpense.create_bulk`
        """

        data = {
            "date": expense_date,
            "title": title,
            "quantity": quantity,
            "unit": unit,
            "unit_price": unit_price,
            "unit_cost": unit_cost,
        }

        for date_key in ["date"]:
            if isinstance(data[date_key], datetime.date):
                data[date_key] = self._convert_date_to_iso(data[date_key])

        for key, value in (
            ("description", description),
            ("billable", billable),
            ("budget_relevant", budget_relevant)
        ):
            if value is not None:
                data[key] = value

        return data
