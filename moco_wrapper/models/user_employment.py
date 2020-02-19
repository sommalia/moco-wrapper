from .base import MWRAPBase
from ..const import API_PATH

from datetime import date

class UserEmployment(MWRAPBase):
    """class for handling employment schemes (in german "wochenmodell")."""

    def __init__(self, moco):
        self._moco = moco

    def get(
        self,
        id: int
        ):
        """retrieve a single employment

        :param id: id of the employment
        :returns: employment object
        """ 
        return self._moco.get(API_PATH["employment_get"].format(id=id))

    def getlist(
        self,
        from_date: date = None,
        to_date: date = None,
        user_id: int = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
        ):
        """retrieve a list of employments

        :param from_date: starting filter date (format YYYY-MM-DD)
        :param to_date: end filter date (format YYYY-MM-DD)
        :param user_id: user id
        :param sort_by: field to sort results by
        :param sort_order: asc or desc
        :param page: page number (default 1)
        :returns: list of employment objects
        """

        params = {}
        for key, value in (
            ("from", from_date),
            ("to", to_date),
            ("user_id", user_id),
            ("page", page)
        ):
            if value is not None:
                if key in ["from", "to"] and isinstance(value, date):
                    params[key] = value.isoformat()
                else:
                    params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["employment_getlist"], params=params)