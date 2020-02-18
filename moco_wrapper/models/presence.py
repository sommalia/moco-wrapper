from .base import MWRAPBase
from ..const import API_PATH

from datetime import date

class Presence(MWRAPBase):
    """class for handling presences (in german "arbeitszeiten")."""

    def __init__(self, moco):
        self._moco = moco

    def getlist(
        self,
        from_date: date = None,
        to_date: date = None,
        user_id: int = None,
        sort_by: str = None,
        sort_order: str  = 'asc',
        page: int = 1
        ):
        """retrieve all presences

        :param from_date: starting date (must be provided together with to_date) (format YYYY-MM-DD)
        :param to_date: end date (must be provided together with from_date) (format YYYY-MM-DD)
        :param user_id: id of the user
        :param sort_by: field to sort results by
        :param sort_order: asc or desc (default asc)
        :param page: page number (default 1)
        :returns: list of presence objets
        """
        params = {}

        for key, value in (
            ("from", from_date),
            ("to", to_date),
            ("user_id", user_id),
            ("page", page),
        ):
            if value is not None:
                if key in ["from", "to"] and isinstance(value, date):
                    params[key] = value.isoformat()
                else:
                    params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["presence_getlist"], params=params)

    def get(
        self,
        id: int
        ):
        """retrieve a single presence

        :param id: id of the presence
        :returns: a single presence object
        """
        return self._moco.get(API_PATH["presence_get"].format(id=id))

    def create(
        self,
        pres_date: str,
        from_time: str,
        to_time: str = None
        ):
        """create a presence

        :param pres_date: date of the presence (format YYYY-MM-DD), or date object
        :param from_time: starting time of the presence (format HH:MM)
        :param to_time: end time of the presence (format HH:MM)
        :returns: the created presence 
        """
        data = {
            'from': from_time,
            'to': to_time,
        }

        if isinstance(pres_date, date):
            data["date"] = pres_date.isoformat()
        else:
            data["date"] = pres_date

        return self._moco.post(API_PATH["presence_create"], data=data)

    def touch(
        self,
        ):
        """creates a new presence for the user with the corresponding api key starting from the current time. Or it terminates an existing open presence at the current time. Can be used to implement a clock system (RFID)

        if a presence is started and stopped within the same minute, it will be discarded
        """ 
        return self._moco.post(API_PATH["presence_touch"])

    def update(
        self,
        id: int,
        pres_date: date = None,
        from_time: str = None,
        to_time: str = None
        ):
        """update a presence

        :param id: id of the presence
        :param pres_date: date of the presence
        :param from_time: starting time of the presence (format HH:MM)
        :param to_time: end time of the presence (format HH:MM)
        :returns: the created presence 
        """
        data = {}
        for key, value in (
            ("date", pres_date),
            ("from", from_time),
            ("to", to_time),
        ):
            if value is not None:
                if key in ["date"] and isinstance(value, date):
                    data[key] = value.isoformat()
                else:
                    data[key] = value

        return self._moco.put(API_PATH["presence_update"].format(id=id), data=data)
        
    def delete(
        self,
        id: int
        ):
        """deletes a presence

        :param id: id of the presence
        """
        return self._moco.delete(API_PATH["presence_delete"].format(id=id))


