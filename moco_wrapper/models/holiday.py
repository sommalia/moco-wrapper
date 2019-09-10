from ..const import API_PATH
from .base import MocoBase

class Holiday(MocoBase):
    """class for handling holidays (in german urlaubsanspruch)."""

    def __init__(self, moco):
        self._moco = moco