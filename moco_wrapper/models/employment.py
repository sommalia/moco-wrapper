from ..const import API_PATH
from .base import MocoBase

class Employment(MocoBase):
    """class for handling employment schemes (in german "wochenmodell")."""

    def __init__(self, moco):
        self._moco = moco