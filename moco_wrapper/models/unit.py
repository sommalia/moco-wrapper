from .base import MocoBase
from ..const import API_PATH

class Unit(MocoBase):
    """Class for handling units/teams."""

    def __init__(self, moco):
        self._moco = moco


    def get(
        self,
        id
        ):
        """Get a single team

        :param id: id of the team
        :returns: team object
        """

        return self._moco.get(API_PATH["unit_get"].format(id=id))

    def getlist(
        self
        sort_by = None,
        sort_order = 'asc'
        ):
        """Get a list of teams
        
        :param sort_by: Sort by field
        :param sort_order: asc or desc
        :returns: list of team objects
        """

        params = {}
        if sort_order is not None:
            params["sort_order"] = "{} {}".format(sort_order, sort_by)

        return self._moco.get(API_PATH["unit_getlist"], params=params)



    