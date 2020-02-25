import datetime

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH

from enum import Enum

class ActivityRemoteService(str, Enum):
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

    def __init__(self, moco):
        self._moco = moco

    def getlist(
        self,
        from_date: datetime.date,
        to_date: datetime.date,
        user_id: int = None,
        project_id: int = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1,
        ):
        """get a list of activity objects

        either the from or the to parameter must be supplied

        :param from_date: start date
        :param to_date: end date
        :param user_id: user id
        :param project_id: project the activity belongs to
        :param sort_by: field to sort results by
        :param sort_order: asc or desc
        :param page: page number (default 1)
        :returns: list of activities
        """

        params = {}

        if isinstance(from_date, datetime.date):
            params["from"] = self.convert_date_to_iso(from_date)
        else:
            params["from"] = from_date

        if isinstance(to_date,  datetime.date):
            params["to"] = self.convert_date_to_iso(to_date)
        else:
            params["to"] = to_date

        for key, value in (
            ("user_id", user_id),
            ("project_id", project_id),
            ("page", page)
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["activity_getlist"], params=params)

    def get(
        self,
        id: int
        ):
        """get a single avctivity

        :param id: id of the acitivity:
        :returns: the activity object

        """

        return self._moco.get(API_PATH["activity_get"].format(id=id))

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
        """create an activity

        :param activity_date: date of the activity
        :parma project_id: id of the project this activity belongs to
        :param task_id: id of the task this activity belongs to (see project tasks)
        :param hours: hours to log to the activity (passing a 0 will start a timer if the date is today)
        :param description: activity description text
        :param billable: true/false (if this activity is billable) (select none if billing is dependent on project configuration)
        :param tag: a tag string
        :param remote_server: if this task was created by a remote service, its name will be here. Allowed values are "trello", "jira", "asana", "basecamp", "wunderlist", "basecamp2", "basecamp3", "toggl", "mite", "github", "youtrack"
        :param remote_id: id of the activity in the remote_service
        :param remote_url: address of the remote service
        :returns: the created activity
        """

        data = {
            "project_id": project_id,
            "task_id" : task_id,
            "hours": hours,
        }
    
        if isinstance(activity_date, datetime.date):
            data["date"] = self.convert_date_to_iso(activity_date)
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
        id: int,
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
        """create an activity

        :param id: id of the activity
        :param activity_date: date of the activity
        :param project_id: id of the project this activity belongs to
        :param task_id: id of the task this activity belongs to (see project tasks)
        :param hours: hours to log to the activity (passing a 0 will start a timer if the date is today)
        :param description: activity description text
        :param billable: true/false (if this activity is billable) (select none if billing is dependent on project configuration)
        :param tag: a tag string
        :param remote_server: if this task was created by a remote service, its name will be here. Allowed values are "trello", "jira", "asana", "basecamp", "wunderlist", "basecamp2", "basecamp3", "toggl", "mite", "github", "youtrack"
        :param remote_id: id of the activity in the remote_service
        :param remote_url: address of the remote service
        :returns: the created activity
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
                    data[key] = self.convert_date_to_iso(value)
                else:
                    data[key] = value

        return self._moco.put(API_PATH["activity_update"].format(id=id), data=data)

    def start_timer(
        self,
        id: int
        ):
        """start a time on the specified activity

        the timer can only be started for activities on the current day

        :param id: id of the activity
        :returns: the activity the timer was started for
        """

        return self._moco.patch(API_PATH["activity_start_timer"].format(id=id))

    def stop_timer(
        self,
        id: int
        ):
        """stop a timer on the specified activity

        :param id: id of the activity
        :returns: the activity the timer was stopped for
        """

        return self._moco.patch(API_PATH["activity_stop_timer"].format(id=id))

    def delete(
        self,
        id: int
        ):
        """delete an activity

        :param id: id of the activity to delete
        """

        return self._moco.delete(API_PATH["activity_delete"].format(id=id))

    def disregard(
        self,
        reason,
        activity_ids,
        company_id,
        project_id = None
        ):
        """mark one or more activities as "already billed"

        :param reason: reason text for disregarding the activities
        :param activity_ids: array of activity ids to disregard
        :param company_id: customer id these activities belong to
        :param project_id: project id these activities belong to  
        :returns: list with the acitivity id that were disregarded
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
