from .base import MWRAPBase
from ..const import API_PATH

class Presence(MWRAPBase):
    """class for handling presences (in german "arbeitszeiten")."""

    def __init__(self, moco):
        self._moco = moco

    def getlist(
        self,
        from_date = None,
        to_date = None,
        user_id = None,
        sort_by = None,
        sort_order = 'asc',
        page = 1
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
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["presence_getlist"], params=params)

    def get(
        self,
        id
        ):
        """retrieve a single presence

        :param id: id of the presence
        :returns: a single presence object
        """
        return self._moco.get(API_PATH["presence_get"].format(id=id))

    def create(
        self,
        date,
        from_time,
        to_time = None
        ):
        """create a presence

        :param date: date of the presence (format YYYY-MM-DD)
        :param from_time: starting time of the presence (format HH:MM)
        :param to_time: end time of the presence (format HH:MM)
        :returns: the created presence 
        """
        data = {
            "date": date,
            "from": from_time
        }

        for key, value in (
            ("to", to_time),
        ):
            if value is not None:
                data[key] = value

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
        id,
        date = None,
        from_time = None,
        to_time = None
        ):
        """update a presence

        :param id: id of the presence
        :param date: date of the presence (format YYYY-MM-DD)
        :param from_time: starting time of the presence (format HH:MM)
        :param to_time: end time of the presence (format HH:MM)
        :returns: the created presence 
        """
        data = {}
        for key, value in (
            ("date", date),
            ("from", from_time),
            ("to", to_time),
        ):
            if value is not None:
                data[key] = value

        return self._moco.put(API_PATH["presence_update"].format(id=id), data=data)
        
    def delete(
        self,
        id
        ):
        """deletes a presence

        :param id: id of the presence
        """
        return self._moco.delete(API_PATH["presence_delete"].format(id=id))


