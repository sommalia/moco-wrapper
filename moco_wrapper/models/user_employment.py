import datetime
from typing import List

from moco_wrapper.util.endpoint import Endpoint
from moco_wrapper.models import objector_models as om
from moco_wrapper.models.base import MWRAPBase


class UserEmployment(MWRAPBase):
    """
    Class for handling user employment schemes.

    Every user has an employment entry, which defines how many hours every day he should be at work.
    """

    @staticmethod
    def endpoints() -> List[Endpoint]:
        """
        Returns all endpoints associated with the model

        :returns: List of Endpoint objects
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`

        """
        return [
            Endpoint("employment_get", "/users/employments/{id}", "GET", om.UserEmployment),
            Endpoint("employment_getlist", "/users/employments", "GET", om.UserEmployment),
            Endpoint("employment_create", "/users/employments", "POST", om.UserEmployment),
            Endpoint("employment_delete", "/users/employments/{id}", "DELETE", om.UserEmployment)
        ]

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def get(
        self,
        employment_id: int
    ):
        """
        Retrieve a single employment:

        :param employment_id: Id of the employment

        :type employment_id: int

        :returns: Employment object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "id": employment_id
        }

        return self._moco.get("employment_get", ep_params=ep_params)

    def getlist(
        self,
        from_date: datetime.date = None,
        to_date: datetime.date = None,
        user_id: int = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Retrieve a list of employments.

        :param from_date: Start date (default ``None``)
        :param to_date: End date (default ``None``)
        :param user_id: User id (default ``None``)
        :param sort_by: Field to sort results by (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type from_date: datetime.date, str
        :type to_date: datetime.date, str
        :type user_id: int
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of employment objects
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`
        """

        params = {}
        for key, value in (
            ("from", from_date),
            ("to", to_date),
            ("user_id", user_id),
            ("page", page)
        ):
            if value is not None:
                if key in ["from", "to"] and isinstance(value, datetime.date):
                    params[key] = self._convert_date_to_iso(value)
                else:
                    params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get("employment_getlist", params=params)

    def create(
        self,
        user_id: int,
        pattern: dict,
        from_date: datetime.date,
        to_date: datetime.date = None,
    ):
        """
        Creates an user employment

        :param user_id: Id of the user to create the employment for
        :param pattern: Work hours during the morning and the afternoon on each workday
        :param from_date: When employment comes into effect
        :param to_date: When the employment stops being in effect default (``None``)

        :type user_id: int
        :type pattern: dict
        :type from_date: datetime, str
        :type to_date: datetime, str

        .. code-block:: python

            from moco_wrapper import Moco

            user_id = 123
            pattern = {
                "am": [4,4,4,4,4],
                "pm": [4,4,4,4,4]
            }

            m = Moco()
            new_schedule = m.UserEmployment.create(
                user_id=user_id,
                pattern=pattern
            )
        """

        data = {
            "user_id": user_id,
            "pattern": pattern,
            "from": from_date,
        }

        # overwrite all date fields in data with isoformat for required fields
        for date_key in ["from"]:
            if isinstance(data[date_key], datetime.date):
                data[date_key] = self._convert_date_to_iso(data[date_key])


        for key, value in (
            ("to", to_date),
        ):
            if value is not None:
                if key in ["from", "to"] and isinstance(value, datetime.date):
                    data[key] = self._convert_date_to_iso(value)
                else:
                    data[key] = value

        print(data)

        return self._moco.post("employment_create", data=data)

    def delete(
        self,
        employment_id,
    ):
        """
        Deletes an user employment

        :param employment_id: Employment to delete

        :type employment_id: int
        """

        ep_params = {
            "id" : employment_id
        }

        return self._moco.delete("employment_delete", ep_params=ep_params)





