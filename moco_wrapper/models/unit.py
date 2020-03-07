from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH

class Unit(MWRAPBase):
    """
    Class for handling teams.
    
    When a user is created he always belongs to a team (e.g. development). These can be managed with this model.
    """

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco


    def get(
        self,
        unit_id: int
        ):
        """
        Get a single team.

        :param unit_id: Id of the team

        :type unit_id: int

        :returns: Single team object
        """

        return self._moco.get(API_PATH["unit_get"].format(id=unit_id))

    def getlist(
        self,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
        ):
        """
        Retrieve a list of teams.
        
        :param sort_by: Sort by field
        :param sort_order: asc or desc (default asc)
        :param page: page number (default 1)

        :type sort_by: str
        :type sort_order: str
        :type page: int
        
        :returns: List of team objects
        """

        params = {}

        for key, value in (
            ("page", page),
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["unit_getlist"], params=params)



    