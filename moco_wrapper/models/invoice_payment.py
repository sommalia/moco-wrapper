from ..const import API_PATH
from .base import MocoBase

class InvoicePayment(MocoBase):
    """class for handling invoice payments(in german "rechnungen")."""
    def __init__(self, moco):
        self._moco = moco