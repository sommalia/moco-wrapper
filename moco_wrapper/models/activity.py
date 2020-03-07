import datetime

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH

from enum import Enum

class ActivityRemoteService(str, Enum):
    """
    Enumeration for allowed values used that can be supplied for the ``remote_service`` argument in :meth:`.Activity.create` and :meth:`.Activity.update`

    .. code-block:: python

        from moco_wrapper import Moco
        from moco_wrapper.models.activity import ActivityRemoteService

        m = Moco()
        activity_create = m.Activity.create(
            ..
            remote_service = ActivityRemoteService.TRELLO
        )

    """
    TRELLO = "trello"
    JIRA = "jira"
    ASANA = "asana"
    BASECAMP = "basecamp"
    BASECAMP2 = "basecamp2"
    BASECAMP3 = "basecamp3"
    TOGGL = "toggl"
    MITE = "mite"
    GITHUB = "github"
    WUNDERLIST = "wunderlist"
    YOUTRACK = "youtrack"


class Activity(MWRAPBase):
    """
    Class for handling activities.
    
    Activities are always created for a project task. The order of things is `Project>Task>Activity`. An activity always belongs to a task and that task always belongs to a project.

    Example Usage:

    .. code-block:: python

        from moco_wrapper import Moco

        m = Moco()
        project_id = 2
        task_id = 3

        #log time
        created_activity = m.Activity.create(
            datetime.date(2020, 1, 1),
            project_id,
            task_id,
            0.25
            description="did things"
        )
        
    """

    def __init__(self, moco):
        """
        Class constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def getlist(
        self,
        from_date: datetime.date,
        to_date: datetime.date,
        user_id: int = None,
        project_id: int = None,
        task_id: int = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1,
        ):
        """
        Get a list of activity objects.

        :param from_date: Start date
        :param to_date: End date
        :param user_id: User id of the creator
        :param project_id: Id of the project the activity belongs to
        :param task_id: Id of the task the activity belongs t
        :param sort_by: Field to sort results by
        :param sort_order: asc or desc
        :param page: Page number (default 1)

        :type from_date: datetime.date, str
        :type to_date: datetime.date, str
        :type user_id: int
        :type project_id: int
        :type task_id: int
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of activities
        """

        if task_id is not None and project_id is None:
            raise ValueError("If task_id is set, project id must also be set")

        params = {}

        if isinstance(from_date, datetime.date):
            params["from"] = self._convert_date_to_iso(from_date)
        else:
            params["from"] = from_date

        if isinstance(to_date,  datetime.date):
            params["to"] = self._convert_date_to_iso(to_date)
        else:
            params["to"] = to_date


        for key, value in (
            ("user_id", user_id),
            ("project_id", project_id),
            ("task_id", task_id),
            ("page", page)
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["activity_getlist"], params=params)

    def get(
        self,
        activity_id: int
        ):
        """
        Get a single activity.

        :param activity_id: Id of the activity:

        :type activity_id: int

        :returns: The activity object
        """

        return self._moco.get(API_PATH["activity_get"].format(id=activity_id))

    def create(
        self,
        activity_date: datetime.date,
        project_id: int,
        task_id: int,
        hours: float,
        description: str = None,
        billable: bool = None,
        tag: str = None,
        remote_service: str = None,
        remote_id: int = None,
        remote_url: str = None
        ):
        """
        Create an activity.

        :param activity_date: date of the activity
        :param project_id: id of the project this activity belongs to
        :param task_id: id of the task this activity belongs to (see project tasks)
        :param hours: hours to log to the activity (passing a 0 will start a timer if the date is today)
        :param description: activity description text
        :param billable: true/false (if this activity is billable) (select none if billing is dependent on project configuration)
        :param tag: a tag string
        :param remote_service: if this task was created by a remote service, its name will be here.
        :param remote_id: id of the activity in the remote_service
        :param remote_url: address of the remote service

        :type activity_date: datetime.date, str
        :type project_id: int
        :type task_id: int
        :type hours: float
        :type description: str
        :type billable: bool
        :type tag: str
        :type remote_service: :class:`.ActivityRemoteService`, str
        :type remote_id: str
        :type remote_url: str

        :returns: the created activity
        """

        data = {
            "project_id": project_id,
            "task_id" : task_id,
            "hours": hours,
        }
    
        if isinstance(activity_date, datetime.date):
            data["date"] = self._convert_date_to_iso(activity_date)
        else:
            data["date"] = activity_date

        for key, value in (
            ("description", description),
            ("billable", billable),
            ("tag", tag),
            ("remote_service", remote_service),
            ("remote_id", remote_id),
            ("remote_url", remote_url)
        ):
            if value is not None:
                data[key] = value

        return self._moco.post(API_PATH["activity_create"], data=data)

    def update(
        self,
        activity_id: int,
        activity_date: datetime.date = None,
        project_id: int = None,
        task_id: int = None,
        hours: float = None,
        description: str = None,
        billable: bool = None,
        tag: str = None,
        remote_service: str = None,
        remote_id: int = None,
        remote_url: str = None
        ):
        """
        Create an activity.

        :param activity_id: id of the activity
        :param activity_date: date of the activity
        :param project_id: id of the project this activity belongs to
        :param task_id: id of the task this activity belongs to (see project tasks)
        :param hours: hours to log to the activity (passing a 0 will start a timer if the date is today)
        :param description: activity description text
        :param billable: true/false (if this activity is billable) (select none if billing is dependent on project configuration)
        :param tag: a tag string
        :param remote_service: if this task was created by a remote service, its name will be here
        :param remote_id: id of the activity in the remote_service
        :param remote_url: address of the remote service

        :type activity_id: int
        :type activity_date: datetime.date, str
        :type project_id: int
        :type task_id: int
        :type hours: float
        :type description: str
        :type billable: bool
        :type tag: str
        :type remote_service: :class:`.ActivityRemoteService`, str
        :type remote_id: str
        :type remote_url: str

        :returns: the updated activity
        """

        data = {}
        for key, value in (
            ("date", activity_date),
            ("project_id", project_id),
            ("task_id", task_id),
            ("hours", hours),
            ("description", description),
            ("billable", billable),
            ("tag", tag),
            ("remote_service", remote_service),
            ("remote_id", remote_id),
            ("remote_url", remote_url)
        ):
            if value is not None:
                if key in ["date"] and isinstance(value, datetime.date):
                    data[key] = self._convert_date_to_iso(value)
                else:
                    data[key] = value

        return self._moco.put(API_PATH["activity_update"].format(id=activity_id), data=data)

    def start_timer(
        self,
        activity_id: int
        ):
        """
        Start a timer on the specified activity.

        The timer can only be started for activities on the current day.

        :param activity_id: id of the activity

        :type activity_id: int

        :returns: the activity the timer was started for
        """

        return self._moco.patch(API_PATH["activity_start_timer"].format(id=activity_id))

    def stop_timer(
        self,
        activity_id: int
        ):
        """
        Stop a timer on the specified activity.

        :param activity_id: Id of the activity

        :type activity_id: int

        :returns: the activity the timer was stopped for
        """

        return self._moco.patch(API_PATH["activity_stop_timer"].format(id=activity_id))

    def delete(
        self,
        activity_id: int
        ):
        """
        Delete an activity.

        :param activity_id: Id of the activity to delete

        :type activity_id: int

        :returns: empty response on success
        """

        return self._moco.delete(API_PATH["activity_delete"].format(id=activity_id))

    def disregard(
        self,
        reason,
        activity_ids,
        company_id,
        project_id = None
        ):
        """
        Disregard activities.

        :param reason: Reason text for disregarding these activities
        :param activity_ids: List of activity ids to disregard
        :param company_id: Company id these activities belong to
        :param project_id: Project id these activities belong to  

        :type reason: str
        :type activity_ids: list
        :type company_id: int
        :type project_id: int

        :returns: List with the activity ids that were disregarded
        """

        data = {
            "reason" : reason,
            "activity_ids" : activity_ids,
            "company_id": company_id,
        }  

        for key, value in (
            ("project_id", project_id),
        ):
            if value is not None:
                data[key] = value

        return self._moco.post(API_PATH["activity_disregard"], data=data)
