from typing import List

from moco_wrapper.util.endpoint import Endpoint
from moco_wrapper.models import objector_models as om
from moco_wrapper.models.base import MWRAPBase


class Report(MWRAPBase):
    """
    Class for handling Reports
    """

    @staticmethod
    def endpoints() -> List[Endpoint]:
        """
        Returns all endpoints associated with the model

        :returns: List of Endpoint objects
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`

        """
        return [
            Endpoint("report_absences_getlist", "/report/absences", "GET", om.Report)
        ]

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def absences(
        self,
        active: bool = None,
        year: int = None,
    ):
        """
        Retrieves a list of absences per user

        :param active: Include only absences for active users (default ``None``)
        :param year: Year to retrieve the absences for (defaults to the current year) (default ``None``)

        :type active: bool
        :type year: int
        """

        params = {}
        for key, value in (
            ("active", active),
            ("year", year)
        ):
            if value is not None:
                params[key] = value

        return self._moco.get("report_absences_getlist", params=params)
