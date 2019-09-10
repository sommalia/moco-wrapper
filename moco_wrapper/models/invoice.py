from ..const import API_PATH
from .base import MocoBase

class Invoice(MocoBase):
    """Models for handling invoices."""

    def __init__(self, moco):
        self._moco = moco

        