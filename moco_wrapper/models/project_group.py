from typing import List

from moco_wrapper.util.endpoint import Endpoint
from moco_wrapper.models import objector_models as om
from moco_wrapper.models.base import MWRAPBase


class ProjectGroup(MWRAPBase):
    """
    Class for handling project contracts.

    When a user gets assigned to a project, that is called a project contract. This can be done with this model.
    """

    @staticmethod
    def endpoints() -> List[Endpoint]:
        """
        Returns all endpoints associated with the model

        :returns: List of Endpoint objects
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`

        """
        return [
            Endpoint(
                "project_group_get",
                "/projects/groups/{project_group_id}",
                "GET",
                om.ProjectGroup,
            ),
            Endpoint(
                "project_group_getlist",
                "/projects/groups",
                "GET",
                om.ProjectGroup,
            ),
        ]

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def get(
        self,
        project_group_id: int,
    ):
        """
        Retrieve a project group.

        :param project_group_id: Id of the project group

        :type project_id: int

        :returns: The project group object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "project_group_id": project_group_id,
        }

        return self._moco.get("project_group_get", ep_params=ep_params)

    def getlist(self, sort_by: str = None, sort_order: str = "asc", page: int = 1):
        """
        Retrieve all active contracts for a project.

        :param sort_by: Sort by field (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type project_id: int
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of contract objects
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`
        """
        ep_params = {}

        params = {}

        for key, value in (("page", page),):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(
            "project_group_getlist",
            ep_params=ep_params,
            params=params,
        )
