
class SingleInternalRate(object):
    def __init__(
        self,
        year,
        rate
    ):
        self.year = year
        self.rate = rate


class AccountInternalHourlyRate(object):
    def __init__(
        self,
        id: int,
        full_name: str,
        rates: list
    ):
        self.id = id
        self.full_name = full_name
        self.rates = []

        for rate_raw in rates:
            item = SingleInternalRate(**rate_raw)
            self.rates.append(item)
