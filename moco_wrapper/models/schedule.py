from .base import MocoBase
from ..const import API_PATH

class Schedule(MocoBase):
    """Class for handling schedules (german "Planung")."""

    def __init__(self, moco):
        self._moco = moco

    def getlist(
        self,
        from_date = None,
        to_date = None,
        user_id = None,
        project_id = None,
        abscence_code = None,
        sort_by = None,
        sort_order = 'asc'
        ):
        """retrieve all planned events

        :param from_date: starting date (format YYYY-MM-DD)
        :param to_date: end date (format YYYY-MM-DD)
        :param user_id: user id the planned entries are belonging to
        :param project_id: project id
        :param abscence_code: 1,2,3,4 (absence, public holiday, sick day, holiday)
        :param sort_by: field to sort the results by
        :param sort_order: asc or desc
        :returns: list of schedule objects
        """
        params = {}
        for key, value in (
            ("from", from_date),
            ("to", to_date),
            ("user_id", user_id),
            ("project_id", project_id),
            ("absence_code", abscence_code)
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["schedule_getlist"], params=params)

    def get(
        self,
        id
        ):
        """retrieve a single planning entry

        :param id: id of the entry
        :returns: schedule object 
        """
        return self._moco.get(API_PATH["schedule_get"].format(id=id))

    def create(
        self,
        date,
        project_id = None,
        absence_code = None,
        user_id = None,
        am = None,
        pm = None,
        comment = None,
        symbol = None,
        overwrite = None,
        ):
        """creates a new planned entry

        :param date: date of the entry (format YYYY-MM-DD)
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

        data = {
            "date": date
        }

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
        id,
        date = None,
        project_id = None,
        absence_code = None,
        user_id = None,
        am = None,
        pm = None,
        comment = None,
        symbol = None,
        overwrite = None,
        ):
        """updates a planned entry

        :param id: id of the entry to update
        :param date: date of the entry (format YYYY-MM-DD)
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
        data = {}
        
        for key, value in (
            ("date", date),
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

        return self._moco.put(API_PATH["schedule_update"].format(id=id), data=data)

    def delete(
        self,
        id
        ):
        """delete a planned entry

        :param id: id of the entry to delete
        """

        return self._moco.delete(API_PATH["schedule_delete"].format(id=id))
