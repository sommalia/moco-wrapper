from moco_wrapper.models import objector_models as obj
from datetime import date


class User(object):
    def __init__(
        self,
        **kwargs
    ):

        nk = kwargs
        if "unit" in kwargs.keys():
            u = obj.Unit(**kwargs["unit"])

            del nk["unit"]
            nk["unit"] = u

        if "bday" in nk.keys():
            nk["birthday"] = nk["bday"]
            del nk["bday"]

        self.__dict__.update(nk)


class UserPerformanceReport(object):
    def __init__(
        self,
        **kwargs
    ):
        self.annually = AnnualUserPerformance(**kwargs["annually"])
        self.monthly = []

        for monthly_item in kwargs["monthly"]:
            performance_item = MonthlyUserPerformance(**monthly_item)
            self.monthly.append(performance_item)

    def __str__(self):
        template = "UserPerformanceReport(annually={0}, monthly=[{1}])"

        return template.format(
            self.annually,
            ", ".join([str(x) for x in self.monthly])
        )


class AnnualUserPerformance(object):
    def __init__(
        self,
        year: int,
        employment_hours: float,
        target_hours: float,
        hours_tracked_total: float,
        variation: float,
        variation_until_today: float
    ):
        self.year = year
        self.employment_hours = employment_hours
        self.target_hours = target_hours
        self.hours_tracked_total = hours_tracked_total
        self.variation = variation
        self.variation_until_today = variation_until_today

    def __str__(self):
        return "AnnualUserPerformance(year={0}, employment_hours={1}, " \
               "target_hours={2}, hours_tracked_total={3}, variation={4}, " \
               "variation_until_today={5})".format(
            self.year,
            self.employment_hours,
            self.target_hours,
            self.hours_tracked_total,
            self.variation,
            self.variation_until_today
        )


class MonthlyUserPerformance(object):
    def __init__(
        self,
        year: int,
        month: int,
        target_hours: float,
        hours_tracked_total: float,
        variation: float
    ):
        self.year = year
        self.month = month
        self.target_hours = target_hours
        self.hours_tracked_total = hours_tracked_total
        self.variation = variation

    def __str__(self):
        return "MonthlyUserPerformance(year={0}, month={1}, target_hours={2}, " \
               "hours_tracked_total={3}, variation={4})".format(
            self.year,
            self.month,
            self.target_hours,
            self.hours_tracked_total,
            self.variation
        )
