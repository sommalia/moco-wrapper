from ..const import API_PATH
from .base import MocoBase

class Offer(MocoBase):
    """class for handling offers (in german "angebote")."""

    def __init__(self, moco):
        self._moco = moco