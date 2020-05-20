from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH


class PlanningEntry(MWRAPBase):
    """
    Class for handling planning.

    .. note:: This is the new way for handling planning (the old way was with Schedules)
    """

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco


