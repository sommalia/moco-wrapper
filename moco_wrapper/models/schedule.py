from .base import MWRAPBase
from ..const import API_PATH

from datetime import date
from enum import Enum

class ScheduleAbsenceCode(int, Enum):
    UNPLANNED = 1
    PUBLIC_HOLIDAY = 2
    SICK_DAY = 3
    HOLIDAY = 4
    ABSENCE = 5

class ScheduleSymbol(int, Enum):
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

class ScheduleAssignmentType(str, Enum):
    PROJECT = "Project"
    ABSENCE = "Absence"

class Schedule(MWRAPBase):
    """Class for handling schedules (german "Planung")."""

    def __init__(self, moco):
        self._moco = moco

    def getlist(
        self,
        from_date: date = None,
        to_date: date = None,
        user_id: int = None,
        project_id: int = None,
        absence_code: ScheduleAbsenceCode  = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page = 1
        ):
        """retrieve all planned events

        :param from_date: starting date
        :param to_date: end date
        :param user_id: user id the planned entries are belonging to
        :param project_id: project id
        :param absence_code: 1,2,3,4,5 (unplanned absence, public holiday, sick day, holiday, absence)
        :param sort_by: field to sort the results by
        :param sort_order: asc or desc (default asc)
        :param page: page number (default 1)
        :returns: list of schedule objects
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
                if key in ["from", "to"] and isinstance(value, date):
                    params[key] = value.isoformat()
                else:
                    params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["schedule_getlist"], params=params)

    def get(
        self,
        id: int
        ):
        """retrieve a single planning entry

        :param id: id of the entry
        :returns: schedule object 
        """
        return self._moco.get(API_PATH["schedule_get"].format(id=id))

    def create(
        self,
        schedule_date: date,
        project_id: int = None,
        absence_code: ScheduleAbsenceCode = None,
        user_id: int = None,
        am: bool = None,
        pm: bool = None,
        comment: str = None,
        symbol: ScheduleSymbol = None,
        overwrite: bool = None,
        ):
        """creates a new planned entry

        :param schedule_date: date of the entry (format YYYY-MM-DD)
        :param project_id: project id (either project id or absence code must be specified)
        :param absence_code: 1,2,3,4 (absence, public holiday, sick day, holiday) (either project id or absence code must be specified)
        :param user_id: user id
        :param am: morning yes/no
        :param pm: afternoon yes/no
        :param comment: comment text
        :param symbol: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 (home, building, car, graduation cap, cocktail, bells, baby carriage, users, moon , info circle)
        :param overwrite: yes/no overwrite existing entry
        :returns: the created planning entry
        """

        if absence_code is not None and project_id is not None:
            raise ValueError("absence_code and project_id are mutually exclusive (specify one, not both)")
        elif absence_code is None and project_id is None:
            raise ValueError("either abscence_code or project_id must be specified")

        data = {
            "date": schedule_date
        }

        if isinstance(schedule_date, date):
            data["date"] = schedule_date.isoformat()

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
        """updates a planned entry

        :param id: id of the entry to update
        :param date: date of the entry (format YYYY-MM-DD)
        :param project_id: project id (either project id or absence code must be specified)
        :param absence_code: 1,2,3,4 (absence, public holiday, sick day, holiday) (either project id or absence code must be specified)
        :param am: morning yes/no
        :param pm: afternoon yes/no
        :param comment: comment text
        :param symbol: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 (home, building, car, graduation cap, cocktail, bells, baby carriage, users, moon , info circle)
        :param overwrite: yes/no overwrite existing entry
        :returns: the created planning entry
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
        """delete a planned entry

        :param id: id of the entry to delete
        :returns: the deleted entry (no empty response)
        """

        return self._moco.delete(API_PATH["schedule_delete"].format(id=id))
