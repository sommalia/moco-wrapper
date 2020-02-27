import datetime

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH

class UserEmployment(MWRAPBase):
    """
    Class for handling user employment schemes. 
    
    Every user has an employment entry, which defines how many hours every day he should be at work.
    """

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def get(
        self,
        id: int
        ):
        """
        Retrieve a single employment

        :param id: Id of the employment
        :returns: Employment object
        """ 
        return self._moco.get(API_PATH["employment_get"].format(id=id))

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
        Retrieve a list of employments

        :param from_date: Start date
        :param to_date: End date
        :param user_id: User id
        :param sort_by: Field to sort results by
        :param sort_order: asc or desc
        :param page: Page number (default 1)
        :returns: List of employment objects
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

        return self._moco.get(API_PATH["employment_getlist"], params=params)