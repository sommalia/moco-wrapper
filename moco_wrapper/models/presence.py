from ..const import API_PATH
from .base import MocoBase

class Presence(MocoBase):
    """class for handling presences (in german "arbeitszeiten")."""

    def __init__(self, moco):
        self._moco = moco