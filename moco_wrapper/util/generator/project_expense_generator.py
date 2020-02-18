from datetime import date

class ProjectExpenseGenerator(object):

    def generate(
        self,
        expense_date: date,
        title: str,
        quantity: float,
        unit: str,
        unit_price: float,
        unit_cost: float,
        description: str = None,
        billable: bool = True,
        budget_relevant: bool = False
        ):
        """create an item that can be used for creating bulk project expenses

        :param project_id: id of the project to create the expense for
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
        :returns: the created expense object

        use it like this

        .. code-block

        gen = ProjectExpenseGenerator()
        items = [
            gen.generate('2019-10-10', "the title", 5, "the unit", 20, 10),
            gen.generate('2019-10-10', "different title", 5, "another unit", 20, 10,l billable=False, description="the desc", budget_relevant=True),
        ]
        project_id = 2
        moco.ProjectExpense.create_bulk(project_id,items)
        """ 

        data = {
            "date": expense_date,
            "title": title,
            "quantity": quantity,
            "unit": unit,
            "unit_price": unit_price,
            "unit_cost": unit_cost,
        }

        if isinstance(expense_date, date):
            data["date"] = expense_date.isoformat()

        for key, value in (
            ("description", description),
            ("billable", billable),
            ("budget_relevant", budget_relevant)
        ):
            if value is not None:
                data[key] = value

        return data