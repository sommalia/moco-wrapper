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
        ):
        """Get a list of teams
        
        :returns: list of team objects
        """

        return self._moco.get(API_PATH["unit_getlist"])



    