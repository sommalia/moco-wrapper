import datetime
from typing import List

from moco_wrapper.util.endpoint import Endpoint
from moco_wrapper.models import objector_models as om
from moco_wrapper.models.base import MWRAPBase


class UserPresence(MWRAPBase):
    """
    Class for handling presences.

    With this model you can log the times your user start and finish the workday. For example if the users punch in to
    indicate they have arrived and punch out to leave, you can log the times with this model.

    Also this can be used to log when you users are at work.
    """

    @staticmethod
    def endpoints() -> List[Endpoint]:
        """
        Returns all endpoints associated with the model

        :returns: List of Endpoint objects
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`

        """
        return [
            Endpoint("presence_create", "/users/presences", "POST", om.UserPresence),
            Endpoint("presence_update", "/users/presences/{id}", "PUT", om.UserPresence),
            Endpoint("presence_get", "/users/presences/{id}", "GET", om.UserPresence),
            Endpoint("presence_getlist", "/users/presences", "GET", om.UserPresence),
            Endpoint("presence_delete", "/users/presences/{id}", "DELETE"),
            Endpoint("presence_touch", "/users/presences/touch", "POST")
        ]

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def getlist(
        self,
        from_date: datetime.date = None,
        to_date: datetime.date = None,
        user_id: int = None,
        is_home_office: bool = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Retrieve all user presences.

        :param from_date: Start date (default ``None``)
        :param to_date: End date (default ``None``)
        :param user_id: Id of the user (default ``None``)
        :param is_home_office: Flag weather the users works from home (default ``None``)
        :param sort_by: Field to sort results by (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type from_date: datetime.date, str
        :type to_date: datetime.date, str
        :type user_id: int
        :type is_home_office: bool
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of presence objects
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`

        .. note::
            ``from_date`` and ``to_date`` must be provided together.
        """
        params = {}

        for key, value in (
            ("from", from_date),
            ("to", to_date),
            ("user_id", user_id),
            ("page", page),
            ("is_home_office", is_home_office)
        ):
            if value is not None:
                if key in ["from", "to"] and isinstance(value, datetime.date):
                    params[key] = self._convert_date_to_iso(value)
                else:
                    params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get("presence_getlist", params=params)

    def get(
        self,
        pres_id: int
    ):
        """
        Retrieve a single presence.

        :param pres_id: Id of the presence

        :type pres_id: int

        :returns: Single presence object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "id": pres_id
        }

        return self._moco.get("presence_get", ep_params=ep_params)

    def create(
        self,
        pres_date: str,
        from_time: str,
        to_time: str = None,
        is_home_office: bool = None
    ):
        """
        Create a presence.

        :param pres_date: Date of the presence
        :param from_time: Starting time of the presence (format HH:MM)
        :param to_time: End time of the presence (format HH:MM) (default ``None``)
        :param is_home_office: Flag weather the user works from home (default ``None``)

        :type pres_date: datetime.date, str
        :type from_time: str
        :type to_time: str
        :type is_home_office: bool

        :returns: The created presence
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        data = {
            'from': from_time,
            'to': to_time,
        }

        if isinstance(pres_date, datetime.date):
            data["date"] = self._convert_date_to_iso(pres_date)
        else:
            data["date"] = pres_date

        for key, value in (
            ("is_home_office", is_home_office),
        ):
            if value is not None:
                data[key] = value

        return self._moco.post("presence_create", data=data)

    def touch(
        self,
        is_home_office: bool = None
    ):
        """
        Creates a new presence for the user with the corresponding api key starting from the current time.
        Or it terminates an existing open presence at the current time. Can be used to implement a clock system (RFID).

        If a presence is started and stopped within the same minute, it will be discarded.

        :param is_home_office: Flag weather the user works from home (default ``None``)

        :type is_home_office: bool

        :returns: The created presence
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse
        """

        data = {}
        for key, value in (
            ("is_home_office", is_home_office),
        ):
            if value is not None:
                data[key] = value

        return self._moco.post("presence_touch", data=data)

    def update(
        self,
        pres_id: int,
        pres_date: datetime.date = None,
        from_time: str = None,
        to_time: str = None,
        is_home_office: bool = None
    ):
        """
        Update a presence.

        :param pres_id: Id of the presence
        :param pres_date: Date of the presence (default ``None``)
        :param from_time: Starting time of the presence (format HH:MM) (default ``None``)
        :param to_time: End time of the presence (format HH:MM) (default ``None``)
        :param is_home_office: Flag weather the user works from home (default ``None``)

        :type pres_id: int
        :type pres_date: datetime.date, str
        :type from_time: str
        :type to_time: str
        :type is_home_office: bool

        :returns: The updated presence
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "id": pres_id
        }

        data = {}
        for key, value in (
            ("date", pres_date),
            ("from", from_time),
            ("to", to_time),
            ("is_home_office", is_home_office),
        ):
            if value is not None:
                if key in ["date"] and isinstance(value, datetime.date):
                    data[key] = self._convert_date_to_iso(value)
                else:
                    data[key] = value

        return self._moco.put("presence_update", ep_params=ep_params, data=data)

    def delete(
        self,
        pres_id: int
    ):
        """
        Deletes a presence.

        :param pres_id: Id of the presence

        :type pres_id: int

        :returns: Empty response on success
        :rtype: :class:`moco_wrapper.util.response.EmptyResponse`
        """
        ep_params = {
            "id": pres_id
        }

        return self._moco.delete("presence_delete", ep_params=ep_params)
