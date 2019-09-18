from .base import MocoBase
from ..const import API_PATH

class Activity(MocoBase):

    def __init__(self, moco):
        self._moco = moco

    def getlist(
        self,
        from_date = None,
        to_date = None,
        user_id = None,
        project_id = None,
        sort_by = None,
        sort_order = 'asc',
        page = 1,
        ):
        """get a list of acitivty objects

        :param from_date: start date (format YYYY-MM-DD)
        :param to_date: end date (format YYYY-MM-DD)
        :param user_id: user id
        :param project_id: project the activity belongs to
        :param sort_by: field to sort results by
        :param sort_order: asc or desc
        :param page: page number (default 1)
        :returns: list of activities

        """
        params = {}
        for key, value in (
            ("from", from_date),
            ("to", to_date),
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
        id
        ):
        """get a single avctivity

        :param id: id of the acitivity:
        :returns: the activity object

        """

        return self._moco.get(API_PATH["activity_get"].format(id=id))

    def create(
        self,
        date,
        project_id,
        task_id,
        hours,
        description = None,
        billable = None,
        tag = None,
        remote_service = None,
        remote_id = None,
        remote_url = None
        ):
        """create an activity

        :param date: date of the activity (foramt YYYY-MM-DD)
        :parma project_id: id of the project this activity belongs to
        :param task_id: id of the task this activity belongs to (see project tasks)
        :param hours: hours to log to the activity (passing a 0 will start a timer if the date is today)
        :param description: activity description text
        :param billable: true/false (if this activity is billable) (default is true, but will also depend on the project configuration)
        :param tag: a tag string
        :param remote_server: if this task was created by a remote service, its name will be here. Allowed values are "trello", "jira", "asana", "basecamp", "wunderlist", "basecamp2", "basecamp3", "toggl", "mite", "github", "youtrack"
        :param remote_id: id of the activity in the remote_service
        :param remote_url: address of the remote service
        :returns: the created activity
        """

        data = {
            "date" : date,
            "project_id": project_id,
            "task_id" : task_id,
            "hours": hours,
        }

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
        id,
        date = None,
        project_id = None,
        task_id = None,
        hours = None,
        description = None,
        billable = None,
        tag = None,
        remote_service = None,
        remote_id = None,
        remote_url = None
        ):
        """create an activity

        :param id: id of the activity
        :param date: date of the activity (foramt YYYY-MM-DD)
        :param project_id: id of the project this activity belongs to
        :param task_id: id of the task this activity belongs to (see project tasks)
        :param hours: hours to log to the activity (passing a 0 will start a timer if the date is today)
        :param description: activity description text
        :param billable: true/false (if this activity is billable) (default is true, but will also depend on the project configuration)
        :param tag: a tag string
        :param remote_server: if this task was created by a remote service, its name will be here. Allowed values are "trello", "jira", "asana", "basecamp", "wunderlist", "basecamp2", "basecamp3", "toggl", "mite", "github", "youtrack"
        :param remote_id: id of the activity in the remote_service
        :param remote_url: address of the remote service
        :returns: the created activity
        """

        data = {}
        for key, value in (
            ("date", date),
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
                data[key] = value

        return self._moco.put(API_PATH["activity_update"].format(id=id), data=data)

    def start_timer(
        self,
        id
        ):
        """start a time on the specified activity

        the timer can only be started for activities on the current day

        :param id: id of the activity
        """

        return self._moco.patch(API_PATH["activity_start_timer"].format(id=id))

    def stop_timer(
        self,
        id
        ):
        """stop a timer on the specified activity

        :param id: id of the activity
        """

        return self._moco.patch(API_PATH["activity_stop_timer"].format(id=id))

    def delete(
        self,
        id
        ):
        """delete an activity

        :param id: id of the activity to delete
        """

        return self._moco.delete(API_PATH["activity_delete"].format(id=id))

    def disregard(
        self,
        reason,
        activity_ids,
        customer_id,
        project_id
        ):
        """mark one or more activities as "already billed"

        :param reason: reason text for disregarding the activities
        :param activity_ids: array of activity ids to disregard
        :param customer_id: customer id these activities belong to
        :param project_id: project id these activities belong to  
        """

        data = {
            "reason" : reason,
            "activity_ids" : activity_ids,
            "customer_id": customer_id,
            "project_id": project_id
        }  

        return self._moco.post(API_PATH["activity_disregard"], data=data)
