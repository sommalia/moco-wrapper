from ..const import API_PATH
from .base import MocoBase

class ProjectTask(MocoBase):
    """class for handling tasks of a project (in german "leistungen")."""

    def __init__(self, moco):
        self._moco = moco

