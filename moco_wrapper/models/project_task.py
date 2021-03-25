from typing import List

from moco_wrapper.util.endpoint import Endpoint
from moco_wrapper.models import objector_models as om
from moco_wrapper.models.base import MWRAPBase


class ProjectTask(MWRAPBase):
    """
    Class for handling tasks of a project.
    """

    @staticmethod
    def endpoints() -> List[Endpoint]:
        """
        Returns all endpoints associated with the model

        :returns: List of Endpoint objects
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`

        """
        return [
            Endpoint("project_task_create", "/projects/{project_id}/tasks", "POST", om.ProjectTask),
            Endpoint("project_task_update", "/projects/{project_id}/tasks/{task_id}", "PUT", om.ProjectTask),
            Endpoint("project_task_get", "/projects/{project_id}/tasks/{task_id}", "GET", om.ProjectTask),
            Endpoint("project_task_getlist", "/projects/{project_id}/tasks", "GET", om.ProjectTask),
            Endpoint("project_task_delete", "/projects/{project_id}/tasks/{task_id}", "DELETE")
        ]

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def getlist(
        self,
        project_id: int,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Retrieve a list of tasks for a project.

        :param project_id: Id of the project
        :param sort_by: Field to sort results by (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type project_id: int
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of project tasks
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`
        """
        ep_params = {
            "project_id": project_id
        }

        params = {}

        for key, value in (
            ("page", page),
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get("project_task_getlist", ep_params=ep_params, params=params)

    def get(
        self,
        project_id: int,
        task_id: int
    ):
        """
        Retrieve a single project task.

        :param project_id: Id of the project the task belongs to
        :param task_id: Id of the task

        :type project_id: int
        :type task_id: int

        :returns: Single project task
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "project_id": project_id,
            "task_id": task_id
        }

        return self._moco.get("project_task_get", ep_params=ep_params)

    def create(
        self,
        project_id: int,
        name: str,
        billable: bool = True,
        active: bool = True,
        budget: float = None,
        hourly_rate: float = None
    ):
        """
        Create a task for a project.

        :param project_id: Id of the project the created task will belong to
        :param name: Name of the task
        :param billable: If this expense billable (default ``True``)
        :param active: If this expense active (default ``True``)
        :param budget: Budget for the task (e.g. 200.75) (default ``None``)
        :param hourly_rate: How much is the hourly rate for the task (e.g.: 120.5) (default ``None``)

        :type project_id: int
        :type name: str
        :type billable: bool
        :type active: bool
        :type budget: float
        :type hourly_rate: float

        :returns: The created project task
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "project_id": project_id
        }

        data = {
            "name": name
        }

        for key, value in (
            ("billable", billable),
            ("active", active),
            ("budget", budget),
            ("hourly_rate", hourly_rate)
        ):
            if value is not None:
                data[key] = value

        return self._moco.post("project_task_create", ep_params=ep_params, data=data)

    def update(
        self,
        project_id: int,
        task_id: int,
        name: str = None,
        billable: bool = None,
        active: bool = None,
        budget: float = None,
        hourly_rate: float = None
    ):
        """
        Update a task for a project.

        :param project_id: Id of the project the task belongs to
        :param task_id: Id of the task to update
        :param name: Name of the task (default ``None``)
        :param billable: If this expense billable (default ``None``)
        :param active: If this expense active (default ``None``)
        :param budget: Budget for the task (e.g. 200.75) (default ``None``)
        :param hourly_rate: How much is the hourly rate for the task (e.g.: 120.5) (default ``None``)

        :type project_id: int
        :type task_id: int
        :type name: str
        :type billable: bool
        :type active: bool
        :type budget: float
        :type hourly_rate: float

        :returns: The updated project task
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "project_id": project_id,
            "task_id": task_id
        }

        data = {}
        for key, value in (
            ("name", name),
            ("billable", billable),
            ("active", active),
            ("budget", budget),
            ("hourly_rate", hourly_rate)
        ):
            if value is not None:
                data[key] = value

        return self._moco.put("project_task_update", ep_params=ep_params, data=data)

    def delete(
        self,
        project_id: int,
        task_id: int
    ):
        """
        Delete project task.

        :param project_id: Id of the project the task belongs to
        :param task_id: Id of the task to delete

        :type project_id: int
        :type task_id: int

        :returns: Empty response on success
        :rtype: :class:`moco_wrapper.util.response.EmptyResponse`

        .. note::

            Deletion of a task is only possible as long as no hours were tracked for the task
        """
        ep_params = {
            "project_id": project_id,
            "task_id": task_id
        }

        return self._moco.delete("project_task_delete", ep_params=ep_params)
