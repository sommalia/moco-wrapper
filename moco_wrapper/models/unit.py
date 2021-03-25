from typing import List

from moco_wrapper.util.endpoint import Endpoint
from moco_wrapper.models import objector_models as om
from moco_wrapper.models.base import MWRAPBase


class Unit(MWRAPBase):
    """
    Class for handling teams.

    When a user is created he always belongs to a team (e.g. development). These can be managed with this model.
    """

    @staticmethod
    def endpoints() -> List[Endpoint]:
        """
        Returns all endpoints associated with the model

        :returns: List of Endpoint objects
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`

        """
        return [
            Endpoint("unit_get", "/units/{id}", "GET", om.Unit),
            Endpoint("unit_getlist", "/units", "GET", om.Unit)
        ]

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def get(
        self,
        unit_id: int
    ):
        """
        Get a single team.

        :param unit_id: Id of the team

        :type unit_id: int

        :returns: Single team object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "id": unit_id
        }

        return self._moco.get("unit_get", ep_params=ep_params)

    def getlist(
        self,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Retrieve a list of teams.

        :param sort_by: Sort by field (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: page number (default ``1``)

        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of team objects
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`
        """
        params = {}

        for key, value in (
            ("page", page),
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get("unit_getlist", params=params)
