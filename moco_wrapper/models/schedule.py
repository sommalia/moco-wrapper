import datetime

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH

from enum import Enum

class ScheduleAbsenceCode(int, Enum):
    """
    Enumeration for allowed values of argument ``absence_code`` of :meth:`.Schedule.getlist`, :meth:`.Schedule.create` and :meth:`.Schedule.update`

    .. code-block:: python

        from moco_wrapper.models.schedule import ScheduleAbsenceCode
        from moco_wrapper import Moco

        m = Moco()
        new_schedule = m.Schedule.create(
            ..
            absence_code = ScheduleAbsenceCode.SICK_DAY
        )
    """
    UNPLANNED = 1
    PUBLIC_HOLIDAY = 2
    SICK_DAY = 3
    HOLIDAY = 4
    ABSENCE = 5

class ScheduleSymbol(int, Enum):
    """
    Enumeration for allowed values of arguemnt ``symbol`` of :meth:`.Schedule.create` and :meth:`.Schedule.update`

    .. code-block:: python

        from moco_wrapper.models.schedule import ScheduleSymbol
        from moco_wrapper import Moco

        m = Moco()
        new_schedule = m.Schedule.create(
            ..
            symbol = ScheduleSymbol.HOME
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

class ScheduleAssignmentType(object):
    """
    Enumeration for types of schedules that can exist.
    """

    PROJECT = "Project"
    ABSENCE = "Absence"

class Schedule(MWRAPBase):
    """
    Class for handling user schedules.
    """

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
        project_id: int = None,
        absence_code: ScheduleAbsenceCode  = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page = 1
        ):
        """
        Retrieve all planned schedule items.

        :param from_date: Start date
        :param to_date: End date
        :param user_id: user id the planned entries are belonging to
        :param project_id: project id
        :param absence_code: Type of absence. For allowed values see :class:`.ScheduleAbsenceCode`
        :param sort_by: Field to sort the results by
        :param sort_order: asc or desc (default asc)
        :param page: Page number (default 1)
        :returns: List of schedule objects
        """

        params = {}
        for key, value in (
            ("from", from_date),
            ("to", to_date),
            ("user_id", user_id),
            ("project_id", project_id),
            ("absence_code ", absence_code),
            ("page", page),
        ):
            if value is not None:
                if key in ["from", "to"] and isinstance(value, datetime.date):
                    params[key] = self.convert_date_to_iso(value)
                else:
                    params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["schedule_getlist"], params=params)

    def get(
        self,
        id: int
        ):
        """
        Retrieve a single schedule object.

        :param id: Id of the entry
        :returns: Single schedule object 
        """
        return self._moco.get(API_PATH["schedule_get"].format(id=id))

    def create(
        self,
        schedule_date: datetime.date,
        project_id: int = None,
        absence_code: ScheduleAbsenceCode = None,
        user_id: int = None,
        am: bool = None,
        pm: bool = None,
        comment: str = None,
        symbol: ScheduleSymbol = None,
        overwrite: bool = None,
        ):
        """
        Create a new schedule entry.

        :param schedule_date: date of the entry
        :param project_id: Project id
        :param absence_code: Type of absence. For allowed values see :class:`.ScheduleAbsenceCode` 
        :param user_id: User id
        :param am: Morning yes/no
        :param pm: Afternoon yes/no
        :param comment: Comment text
        :param symbol: Symbol to use for the schedule item. For allowed values see :class:`.ScheduleSymbol`
        :param overwrite: yes/no overwrite existing entry
        :returns: The created planning entry

        .. note::

            Define either ``project_id`` OR ``absence_code``, specify one, not both.
        """

        if absence_code is not None and project_id is not None:
            raise ValueError("absence_code and project_id are mutually exclusive (specify one, not both)")
        elif absence_code is None and project_id is None:
            raise ValueError("Either abscence_code or project_id must be specified")

        data = {
            "date": schedule_date
        }

        for date_key in ["date"]:
            if isinstance(data[date_key], datetime.date):
                data[date_key] = self.convert_date_to_iso(data[date_key])

        for key, value in (
            ("project_id", project_id),
            ("absence_code", absence_code),
            ("user_id", user_id),
            ("am", am),
            ("pm", pm),
            ("comment", comment),
            ("symbol", symbol),
            ("overwrite", overwrite)
        ):
            if value is not None:
                data[key] = value

        return self._moco.post(API_PATH["schedule_create"], data=data)

    def update(
        self,
        id: int,
        project_id: int = None,
        absence_code: ScheduleAbsenceCode = None,
        am: bool = None,
        pm: bool = None,
        comment: str = None,
        symbol: ScheduleSymbol = None,
        overwrite: bool = None,
        ):
        """
        Update a schedule entry.

        :param id: Id of the entry to update
        :param project_id: Project id
        :param absence_code: Type of absence. For allowed values see :class:`.ScheduleAbsenceCode` 
        :param am: Morning yes/no
        :param pm: Afternoon yes/no
        :param comment: Comment text
        :param symbol: Symbol to use for the schedule item. For allowed values see :class:`.ScheduleSymbol`
        :param overwrite: yes/no overwrite existing entry
        :returns: The updated schedule entry

        .. note::

            Define either ``project_id`` OR ``absence_code``, specify one, not both.
        """
        
        if absence_code is not None and project_id is not None:
            raise ValueError("absence_code and project_id are mutually exclusive (specify one, not both)")
        elif absence_code is None and project_id is None:
            raise ValueError("either abscence_code or project_id must be specified")

        data = {}
        
        for key, value in (
            ("project_id", project_id),
            ("absence_code", absence_code),
            ("am", am),
            ("pm", pm),
            ("comment", comment),
            ("symbol", symbol),
            ("overwrite", overwrite)
        ):
            if value is not None:
                data[key] = value

        return self._moco.put(API_PATH["schedule_update"].format(id=id), data=data)

    def delete(
        self,
        id: int
        ):
        """
        Delete a schedule entry.

        :param id: Id of the entry to delete
        :returns: Empty response on success
        """

        return self._moco.delete(API_PATH["schedule_delete"].format(id=id))
