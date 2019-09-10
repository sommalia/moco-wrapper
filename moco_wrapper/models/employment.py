from ..const import API_PATH
from .base import MocoBase

class Employment(MocoBase):
    """class for handling employment schemes (in german "wochenmodell")."""

    def __init__(self, moco):
        self._moco = moco

    def get(
        self,
        id
        ):
        """retrieve a single employment

        :param id: id of the employment
        :returns: employment object
        """ 
        return self._moco.get(API_PATH["employment_get"].format(id=id))

    def getlist(
        self,
        from_date = None,
        to_date = None,
        user_id = None,
        sort_by = None,
        sort_order = 'asc'
        ):
        """retrieve a list of employments

        :param from_date: starting filter date (format YYYY-MM-DD)
        :param to_date: end filter date (format YYYY-MM-DD)
        :param user_id: user id
        :param sort_by: field to sort results by
        :param sort_order: asc or desc
        :returns: list of employment objects
        """

        params = {}
        for key, value in (
            ("from", from_date),
            ("to", to_date),
            ("user_id", user_id),
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["employment_getlist"], params=params)