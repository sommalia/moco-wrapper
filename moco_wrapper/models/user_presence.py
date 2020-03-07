import datetime

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH

class UserPresence(MWRAPBase):
    """
    Class for handling presences.

    With this model you can log the times your user start and finish the workday. For example if the users punch in to indicate they have arrived and punch out to leave, you can log the times with this model.

    Also this can be used to log when you users are at work.
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
        sort_by: str = None,
        sort_order: str  = 'asc',
        page: int = 1
        ):
        """
        Retrieve all user presences.

        :param from_date: Start date
        :param to_date: End date
        :param user_id: Id of the user
        :param sort_by: Field to sort results by
        :param sort_order: asc or desc (default asc)
        :param page: Page number (default 1)

        :type from_date: datetime.date, str
        :type to_date: datetime.date, str
        :type user_id: int
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of presence objets

        .. note::

            ``from_date`` and ``to_date`` must be provided together.
        """
        params = {}

        for key, value in (
            ("from", from_date),
            ("to", to_date),
            ("user_id", user_id),
            ("page", page),
        ):
            if value is not None:
                if key in ["from", "to"] and isinstance(value, datetime.date):
                    params[key] = self._convert_date_to_iso(value)
                else:
                    params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["presence_getlist"], params=params)

    def get(
        self,
        pres_id: int
        ):
        """
        Retrieve a single presence.

        :param pres_id: Id of the presence

        :type pres_id: int

        :returns: Single presence object
        """
        return self._moco.get(API_PATH["presence_get"].format(id=pres_id))

    def create(
        self,
        pres_date: str,
        from_time: str,
        to_time: str = None
        ):
        """
        Create a presence.

        :param pres_date: Date of the presence
        :param from_time: Starting time of the presence (format HH:MM)
        :param to_time: End time of the presence (format HH:MM)

        :type pres_date: datetime.date, str
        :type from_time: str
        :type to_time: str

        :returns: The created presence 
        """
        data = {
            'from': from_time,
            'to': to_time,
        }

        if isinstance(pres_date, datetime.date):
            data["date"] = self._convert_date_to_iso(pres_date)
        else:
            data["date"] = pres_date

        return self._moco.post(API_PATH["presence_create"], data=data)

    def touch(
        self,
        ):
        """
        Creates a new presence for the user with the corresponding api key starting from the current time. Or it terminates an existing open presence at the current time. Can be used to implement a clock system (RFID).

        If a presence is started and stopped within the same minute, it will be discarded.
        """ 
        return self._moco.post(API_PATH["presence_touch"])

    def update(
        self,
        pres_id: int,
        pres_date: datetime.date = None,
        from_time: str = None,
        to_time: str = None
        ):
        """
        Update a presence.

        :param pres_id: Id of the presence
        :param pres_date: Date of the presence
        :param from_time: Starting time of the presence (format HH:MM)
        :param to_time: End time of the presence (format HH:MM)

        :type pres_id: int
        :type pres_date: datetime.date, str
        :type from_time: str
        :type to_time: str

        :returns: The created presence 
        """
        data = {}
        for key, value in (
            ("date", pres_date),
            ("from", from_time),
            ("to", to_time),
        ):
            if value is not None:
                if key in ["date"] and isinstance(value, datetime.date):
                    data[key] = self._convert_date_to_iso(value)
                else:
                    data[key] = value

        return self._moco.put(API_PATH["presence_update"].format(id=pres_id), data=data)
        
    def delete(
        self,
        pres_id: int
        ):
        """
        Deletes a presence.

        :param pres_id: Id of the presence

        :type pres_id: int

        :returns: Empty response on success
        """
        return self._moco.delete(API_PATH["presence_delete"].format(id=pres_id))
        