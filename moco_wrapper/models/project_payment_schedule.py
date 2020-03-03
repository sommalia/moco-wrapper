import datetime

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH

class ProjectPaymentSchedule(MWRAPBase):
    """
    Class for handling billing schedules for fixed price projects
    
    Fixed Price projects can have a target date they should be billed on (in the future). With this class you can create this target entry (and how much should be billed).

    For Example you can create a project that will be billed in four (4) steps over the year.

    .. code-block:: python

        from moco_wrapper import Moco

        m = Moco()
        leader_id = 1
        customer_id = 2

        #create fixed price projects
        project = m.Project.create(
            "my fixed price project",
            "EUR",
            leader_id,
            customer_id,
            fixed_price=True,
            budget=4000
        ).data

        first_payment = ProjectPaymentSchedule.create(project.id, 1000.0, date(2020, 3, 1))
        second_payment = ProjectPaymentSchedule.create(project.id, 1000.0, date(2020, 6, 1))
        third_payment = ProjectPaymentSchedule.create(project.id, 1000.0, date(2020, 9, 1))
        fourth_payment = ProjectPaymentSchedule.create(project.id, 1000.0, date(2020, 12, 1))
    """

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self.moco = moco

    def create(
        self,
        project_id: int,
        net_total: float,
        schedule_date: datetime.date,
        title: str = None,
        checked: bool = False,
        ):
        """
        Creates a new project payment schedule

        :oaran project_id: The id of the project the entry belongs to
        :param net_total: How much should be billed on this schedule
        :param schedule_date: Date of the entry
        :param title: Title string
        :param checked: Mark entry as checked
        :returns: The created schedule item
        """

        data = {
            "net_total": net_total,
            "date": schedule_date
        }

        for date_key in ["date"]:
            if isinstance(data[date_key], datetime.date):
                data[date_key] = self._convert_date_to_iso(data[date_key])

        for key, value in (
            ("title", title),
            ("checked", checked)
        ):
            if value is not None:
                data[key] = value

        return self.moco.post(API_PATH["project_payment_schedule_create"].format(project_id=project_id), data=data)