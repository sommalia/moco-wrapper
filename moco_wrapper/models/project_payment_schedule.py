import datetime
from typing import List

from moco_wrapper.util.endpoint import Endpoint
from moco_wrapper.models import objector_models as om
from moco_wrapper.models.base import MWRAPBase


class ProjectPaymentSchedule(MWRAPBase):
    """
    Class for handling billing schedules for fixed price projects.

    Fixed Price projects can have a target date they should be billed on (in the future). With this class you can
    create this target entry (and how much should be billed).

    For Example you can create a project that will be billed in four (4) steps over the year.

    .. code-block:: python

        from moco_wrapper import Moco
        from datetime import date

        m = Moco()

        # create fixed price project
        project = m.Project.create(
            name="my fixed price project",
            currency="EUR",
            leader_id=1,
            customer_id=2,
            fixed_price=True,
            budget=4000
        ).data

        first_payment = m.ProjectPaymentSchedule.create(project.id, 1000.0, date(2020, 3, 1))
        second_payment = m.ProjectPaymentSchedule.create(project.id, 1000.0, date(2020, 6, 1))
        third_payment = m.ProjectPaymentSchedule.create(project.id, 1000.0, date(2020, 9, 1))
        fourth_payment = m.ProjectPaymentSchedule.create(project.id, 1000.0, date(2020, 12, 1))

    .. seealso::
        :meth:`moco_wrapper.models.Project.create`
    """

    @staticmethod
    def endpoints() -> List[Endpoint]:
        """
        Returns all endpoints associated with the model

        :returns: List of Endpoint objects
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`

        """
        return [
            Endpoint("project_payment_schedule_create", "/projects/{project_id}/payment_schedules", "POST",
                     om.ProjectPaymentSchedule),
            Endpoint("project_payment_schedule_update", "/projects/{project_id}/payment_schedules/{schedule_id}",
                     "PUT", om.ProjectPaymentSchedule),
            Endpoint("project_payment_schedule_get", "/projects/{project_id}/payment_schedules/{schedule_id}", "GET",
                     om.ProjectPaymentSchedule),
            Endpoint("project_payment_schedule_getlist", "/projects/{project_id}/payment_schedules", "GET",
                     om.ProjectPaymentSchedule),
            Endpoint("project_payment_schedule_delete", "/projects/{project_id}/payment_schedules/{schedule_id}",
                     "DELETE")
        ]

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def create(
        self,
        project_id: int,
        net_total: float,
        schedule_date: datetime.date,
        title: str = None,
        checked: bool = False,
    ):
        """
        Creates a new project payment schedule.

        :param project_id: The id of the project the entry belongs to
        :param net_total: How much should be billed on this schedule
        :param schedule_date: Date of the entry
        :param title: Title string (default ``None``)
        :param checked: Mark entry as checked (the entry will be crossed out in the UI) (default ``False``)

        :type project_id: int
        :type net_total: float
        :type schedule_date: datetime.date, str
        :type title: str
        :type checked: bool

        :returns: The created schedule item
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "project_id": project_id
        }

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

        return self._moco.post("project_payment_schedule_create", ep_params=ep_params, data=data)

    def update(
        self,
        project_id: int,
        schedule_id: int,
        net_total: float = None,
        schedule_date: datetime.date = None,
        title: str = None,
        checked: bool = None
    ):
        """
        Updates an existing project payment schedule.

        :param project_id: Project id the schedule item belongs to
        :param schedule_id: Id of the schedule item to update
        :param net_total: Total amount to be billed (default ``None``)
        :param schedule_date: Date the billing will take place (default ``None``)
        :param title: Title of the item (default ``None``)
        :param checked: Mark entry as checked (the entry will be crossed out in the UI) (default ``None``)

        :type project_id: int
        :type schedule_id: int
        :type net_total: float
        :type schedule_date: datetime.date, str
        :type title: str
        :type checked: bool

        :returns: The updated schedule item
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "project_id": project_id,
            "schedule_id": schedule_id
        }

        data = {}

        for key, value in (
            ("net_total", net_total),
            ("date", schedule_date),
            ("title", title),
            ("checked", checked),
        ):
            if value is not None:
                if key in ["date"] and isinstance(value, datetime.date):
                    data[key] = self._convert_date_to_iso(value)
                else:
                    data[key] = value

        return self._moco.put("project_payment_schedule_update", ep_params=ep_params, data=data)

    def get(
        self,
        project_id: int,
        schedule_id: int,
    ):
        """
        Retrieves project payment schedule.

        :param project_id: Id of the project to schedule item belongs to
        :param schedule_id: Id of the schedule to retrieve

        :type project_id: int
        :type schedule_id: int

        :returns: The schedule item
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "project_id": project_id,
            "schedule_id": schedule_id
        }

        return self._moco.get("project_payment_schedule_get", ep_params=ep_params)

    def getlist(
        self,
        project_id: int,
    ):
        """
        Retrieve a list of project payment schedules

        :param project_id: Project id of the schedule items

        :type project_id: int

        :returns: List of schedules payments
        :rtype: :class:`moco_wrapper.util.response.ListResponse`
        """
        ep_params = {
            "project_id": project_id
        }

        return self._moco.get("project_payment_schedule_getlist", ep_params=ep_params)

    def delete(
        self,
        project_id: int,
        schedule_id: int
    ):
        """
        Delete a project payment schedule item

        :param project_id: Project the payment schedule belongs to
        :param schedule_id: Id of the schedule item to delete

        :type project_id: int
        :type schedule_id: int

        :returns: The deleted schedule on success
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """

        ep_params = {
            "project_id": project_id,
            "schedule_id": schedule_id
        }

        return self._moco.delete("project_payment_schedule_delete", ep_params=ep_params)
