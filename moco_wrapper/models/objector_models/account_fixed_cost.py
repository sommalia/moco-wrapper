class FixedCostItem(object):
    def __init__(
        self,
        year: int,
        month: int,
        amount: float
    ):
        self.year = year
        self.month = month
        self.amount = amount

    def __str__(self):
        return "FixedCostItem(year={0}, month={1}, amount={2})".format(
            self.year,
            self.month,
            self.amount
        )


class AccountFixedCost(object):

    def __init__(
        self,
        **kwargs
    ):
        nk = kwargs

        cost_items = []
        for cost in kwargs["costs"]:
            item = FixedCostItem(cost["year"], cost["month"], cost["amount"])
            cost_items.append(item)

        nk["costs"] = cost_items

        self.__dict__.update(nk)
