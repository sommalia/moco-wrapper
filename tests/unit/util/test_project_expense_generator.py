from moco_wrapper.util import ProjectExpenseGenerator

class TestProjectExpenseGenerator(object):
    def setup(self):
        self.generator = ProjectExpenseGenerator()

    def test_generate(self):
        date = '2019-10-10'
        title = "more title stuff"
        quantity = 5
        unit = "the unit"
        unit_price = 200
        unit_cost = 150

        description = "the description"
        billable = False
        budget_relevant = True

        data = self.generator.generate(date, title, quantity, unit, unit_price, unit_cost, description=description, billable=billable, budget_relevant=budget_relevant)

        assert data["date"] == date
        assert data["title"] == title
        assert data["quantity"] == quantity
        assert data["unit"] == unit
        assert data["unit_price"] == unit_price
        assert data["unit_cost"] == unit_cost
        assert data["description"] == description
        assert data["billable"] == billable
        assert data["budget_relevant"] == budget_relevant

    def test_generate_default_billable(self):
        billable_default = True

        date = '2019-10-10'
        title = "more title stuff"
        quantity = 5
        unit = "the unit"
        unit_price = 200
        unit_cost = 150

        data = self.generator.generate(date, title, quantity, unit, unit_price, unit_cost)

        assert data["billable"] == billable_default

    def test_generate_default_budget_relevant(self):
        budget_relevant_default = False

        date = '2019-10-10'
        title = "more title stuff"
        quantity = 5
        unit = "the unit"
        unit_price = 200
        unit_cost = 150

        data = self.generator.generate(date, title, quantity, unit, unit_price, unit_cost)

        assert data["budget_relevant"] == budget_relevant_default
