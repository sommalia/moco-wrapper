from ..const import API_PATH
from .base import MocoBase

class ProjectTask(MocoBase):
    """class for handling tasks of a project (in german "leistungen")."""

    def __init__(self, moco):
        self._moco = moco

    def getlist(
        self,
        project_id,
        sort_by = None,
        sort_order = 'asc',
        page = 1
        ):
        """retrieve a list of task for a project

        :param project_id: id of the project
        :param sort_by: field to sort results by
        :param sort_order: asc or desc (default asc)
        :param page: page number (default 1)
        :returns: list of project tasks
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
        project_id,
        task_id
        ):
        """retrieve a single project task

        :param project_id: id of the project the task belongs to
        :param task:id: id of the task
        :returns: a single project task
        """
        return self._moco.get(API_PATH["project_task_get"].format(project_id=project_id, task_id=task_id))

    def create(
        self,
        project_id,
        name,
        billable = None,
        active = None,
        budget = None,
        hourly_rate = None
        ):
        """create a task on a project

        :param project_id: id of the project the created task will belong to
        :param name: name of the task
        :param billable: true/false, if this task is billable or not
        :param active: true/false, if this task is active or not
        :param budget: how much budget for the task (ex: 200)
        :param hourly_rate: how much is the hourly rate for the task (ex: 120)
        :returns: the created project task
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
        project_id,
        task_id,
        name = None,
        billable = None,
        active = None,
        budget = None,
        hourly_rate = None
        ):
        """update a task on a project

        :param project_id: id of the project the task belongs to
        :param task_id: id of the task to update
        :param name: name of the task
        :param billable: true/false, if this task is billable or not
        :param active: true/false, if this task is active or not
        :param budget: how much budget for the task (ex: 200)
        :param hourly_rate: how much is the hourly rate for the task (ex: 120)
        :returns: the created project task
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
        project_id,
        task_id
        ):
        """deletes a task on a projects

        only possible as long as no hours were tracked on the task yet
        """

        return self._moco.delete(API_PATH["project_task_delete"].format(project_id=project_id, task_id=task_id))

