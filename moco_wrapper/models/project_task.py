from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH


class ProjectTask(MWRAPBase):
    """
    Class for handling tasks of a project.
    """

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
        :param sort_by: Field to sort results by
        :param sort_order: asc or desc (default asc)
        :param page: Page number (default 1)

        :type project_id: int
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of project tasks
        """
        params = {}

        for key, value in (
            ("page", page),
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["project_task_getlist"].format(project_id=project_id), params=params)

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
        """
        return self._moco.get(API_PATH["project_task_get"].format(project_id=project_id, task_id=task_id))

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
        :param billable: If this expense billable (default True)
        :param active: If this expense active (default True)
        :param budget: Budget for the task (e.g. 200.75)
        :param hourly_rate: How much is the hourly rate for the task (e.g.: 120.5)

        :type project_id: int
        :type name: str
        :type billable: bool
        :type active: bool
        :type budget: float
        :type hourly_rate: float

        :returns: The created project task
        """
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

        return self._moco.post(API_PATH["project_task_create"].format(project_id=project_id), data=data)

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
        :param name: Name of the task
        :param billable: If this expense billable (default True)
        :param active: If this expense active (default True)
        :param budget: Budget for the task (e.g. 200.75)
        :param hourly_rate: How much is the hourly rate for the task (e.g.: 120.5)

        :type project_id: int
        :type task_id: int
        :type name: str
        :type billable: bool
        :type active: bool
        :type budget: float
        :type hourly_rate: float

        :returns: The updated project task
        """
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

        return self._moco.put(API_PATH["project_task_update"].format(project_id=project_id, task_id=task_id), data=data)

    def delete(
        self,
        project_id: int,
        task_id: int
    ):
        """
        Delete project task

        :param project_id: Id of the project the task belongs to
        :param task_id: Id of the task to delete

        :type project_id: int
        :type task_id: int

        :returns: Empty response on success

        .. note::

            Deletion of a task is only possible as long as no hours were tracked for the task
        """

        return self._moco.delete(API_PATH["project_task_delete"].format(project_id=project_id, task_id=task_id))
