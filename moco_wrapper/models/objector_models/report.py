from moco_wrapper.models import objector_models as obj


class Report(object):
    def __init__(
        self,
        user,
        total_vacation_days,
        used_vacation_days,
        planned_vacation_days,
        sickdays,
    ):
        self.user = obj.User(**user)
        self.total_vacation_days = total_vacation_days
        self.used_vacation_days = used_vacation_days
        self.planned_vacation_days = planned_vacation_days
        self.sickdays = sickdays
