import datetime

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH

from enum import Enum


class PlanningEntrySymbol(int, Enum):
    """
    Enumeration for allowed values for argument ``symbol`` for :meth:`.PlanningEntry.create`.

    .. code-block:: python

        from moco_wrapper.models.planning_entry import PlanningEntrySymbol
        from moco_wrapper import Moco

        m = Moco()

        new_planning_entry = m.create(
            ..
            symbol = PlanningEntrySymbol.HOME
        )
    """
    HOME = 1
    BUILDING = 2
    CAR = 3
    GRADUATION_CAP = 4
    COCKTAIL = 5
    BELLS = 6
    BABY_CARRIAGE = 7
    USERS = 8
    MOON = 9
    INFO_CIRCLE = 10


class PlanningEntry(MWRAPBase):
    """
    Class for handling planning.

    .. note:: This is the new way for handling planning (the old way was with Schedules)
    """

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def getlist(
        self,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
        user_id: int = None,
        project_id: int = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Retrieve a list of planning entries.

        :param start_date: Start date
            (if ``start_date`` is supplied, `end_date` must also be supplied) (default ``None``)
        :param end_date: End date
            (if `end_date` is supplied, ``start_date`` must also be supplied) (default ``None``)
        :param user_id: User id (default ``None``)
        :param project_id: Project id (default ``None``)
        :param sort_by: Field to sort by (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type start_date: datetime.date, str
        :type end_date: datetime.date, str
        :type user_id: int
        :type project_id: int
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of planning entries
        :rtype: :class:`moco_wrapper.util.response.ListingResponse`
        """

        if start_date is not None and end_date is None:
            raise ValueError("If start_date is set, so must be end_date")

        if end_date is not None and start_date is None:
            raise ValueError("If end_date is set, so must be start_date")

        params = {}

        if start_date is not None and end_date is not None:
            start_date_formatted = ""
            if isinstance(start_date, datetime.date):
                start_date_formatted = self._convert_date_to_iso(start_date)
            else:
                start_date_formatted = start_date

            end_date_formatted = ""
            if isinstance(end_date, datetime.date):
                end_date_formatted = self._convert_date_to_iso(end_date)
            else:
                end_date_formatted = end_date

            params["period"] = "{}:{}".format(start_date_formatted, end_date_formatted)

        for key, value in (
            ("user_id", user_id),
            ("project_id", project_id),
            ("page", page)
        ):
            if value is not None:
                params[key] = value

        # add sort order if set
        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["planning_entry_getlist"], params=params)

    def get(
        self,
        planning_entry_id: int
    ):
        """
        Retrieve a single planning entry.

        :param planning_entry_id: Id the of the entry

        :type planning_entry_id: int

        :returns: Single planning entry
        :rtype: :class:`moco_wrapper.util.response.JsonResponse`
        """

        return self._moco.get(API_PATH["planning_entry_get"].format(id=planning_entry_id))

    def create(
        self,
        project_id: int,
        starts_on: datetime.date,
        ends_on: datetime.date,
        hours_per_day: float,
        user_id: int = None,
        comment: str = None,
        symbol: PlanningEntrySymbol = None
    ):
        """
        Create a new planning entry.

        :param project_id: Project id
        :param starts_on: Start date
        :param ends_on: End date
        :param hours_per_day: Hours per day the planning entry will consume
        :param user_id: User id the planning entry belongs to (default ``None``)
        :param comment: A comment (default ``None``)
        :param symbol: Symbol icon to use (default ``None``)

        :type project_id: int
        :type starts_on: datetime.date, str
        :type ends_on: datetime.date, str
        :type hours_per_day: float
        :type user_id: int
        :type comment: str
        :type symbol: :class:`.PlanningEntrySymbol`, int

        :returns: The created planning entry
        :rtype: :class:`moco_wrapper.util.response.JsonResponse`

        .. note::
            If no ``user_id`` is supplied the entry will be created with the user_id of the executing request
            (the user_id the api key belongs to)

        """

        data = {
            "project_id" : project_id,
            "hours_per_day": hours_per_day,
            "starts_on": starts_on,
            "ends_on": ends_on,
            "comment": ""
        }

        for date_key in ["starts_on", "ends_on"]:
            if isinstance(data[date_key], datetime.date):
                data[date_key] = self._convert_date_to_iso(data[date_key])

        for key, value in (
            ("user_id", user_id),
            ("comment", comment),
            ("symbol", symbol)
        ):
            if value is not None:
                data[key] = value

        return self._moco.post(API_PATH["planning_entry_create"], data=data)

    def update(
        self,
        planning_entry_id: int,
        project_id: int = None,
        starts_on: datetime.date = None,
        ends_on: datetime.date = None,
        hours_per_day: float = None,
        user_id: int = None,
        comment: str = None,
        symbol: PlanningEntrySymbol = None,
    ):
        """
        Updates a planning entry.

        :param planning_entry_id: Id of the entry to update
        :param project_id: Project id (default ``None``)
        :param starts_on: Start date (default ``None``)
        :param ends_on: End date (default ``None``)
        :param hours_per_day: Hours per day the planning entry will consume (default ``None``)
        :param user_id: User id the planning entry belongs to (default ``None``)
        :param comment: A comment (default ``None``)
        :param symbol: Symbol icon to use (default ``None``)

        :type planning_entry_id: int
        :type project_id: int
        :type starts_on: datetime.date, str
        :type ends_on: datetime.date, str
        :type hours_per_day: float
        :type user_id: int
        :type comment: str
        :type symbol: :class:`.PlanningEntrySymbol`, int

        :returns: The updated planning entry
        :rtype: :class:`moco_wrapper.util.response.JsonResponse`
        """

        data = {}

        for key, value in (
            ("project_id", project_id),
            ("starts_on", starts_on),
            ("ends_on", ends_on),
            ("hours_per_day", hours_per_day),
            ("user_id", user_id),
            ("comment", comment),
            ("symbol", symbol)
        ):
            if value is not None:
                if key in ["starts_on", "ends_on"] and isinstance(value, datetime.date):
                    data[key] = self._convert_date_to_iso(value)
                else:
                    data[key] = value

        return self._moco.put(API_PATH["planning_entry_update"].format(id=planning_entry_id), data=data)

    def delete(
        self,
        planning_entry_id: int
    ):
        """
        Delete a planning entry.

        :param planning_entry_id: Id of the entry to delete

        :type planning_entry_id: int

        :returns: The deleted planning entry
        :rtype: :class:`moco_wrapper.util.response.JsonResponse`
        """
        return self._moco.delete(API_PATH["planning_entry_delete"].format(id=planning_entry_id))
