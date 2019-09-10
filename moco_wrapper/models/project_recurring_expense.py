from ..const import API_PATH
from .base import MocoBase

class ProjectRecurringExpense(MocoBase):
    """class for handling recurring expenses of a project."""

    def __init__(self, moco):
        self._moco = moco