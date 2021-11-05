import datetime
from typing import List

from moco_wrapper.util.endpoint import Endpoint
from moco_wrapper.models import objector_models as om
from moco_wrapper.models.base import MWRAPBase

from enum import Enum


class ProjectBillingVariant(str, Enum):
    """
    Enumeration for allowed values of the ``billing_variant`` argument of :meth:`.Project.create`
    and :meth:`.Project.update`.

    Example usage:

    .. code-block:: python

        from moco_wrapper.models.project import ProjectBillingVariant
        from moco_wrapper import Moco

        m = Moco()
        new_project = m.Project.create(
            ..
            billing_variant = ProjectBillingVariant.USER
        )

    """
    PROJECT = "project"
    TASK = "task"
    USER = "user"


class Project(MWRAPBase):
    """
    Class for handling projects.
    """

    @staticmethod
    def endpoints() -> List[Endpoint]:
        """
        Returns all endpoints associated with the model

        :returns: List of Endpoint objects
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`

        """
        return [
            Endpoint("project_create", "/projects", "POST", om.Project),
            Endpoint("project_update", "/projects/{id}", "PUT", om.Project),
            Endpoint("project_archive", "/projects/{id}/archive", "PUT", om.Project),
            Endpoint("project_unarchive", "/projects/{id}/unarchive", "PUT", om.Project),
            Endpoint("project_get", "/projects/{id}", "GET", om.Project),
            Endpoint("project_getlist", "/projects", "GET", om.Project),
            Endpoint("project_assigned", "/projects/assigned", "GET", om.Project),
            Endpoint("project_report", "/projects/{id}/report", "GET", om.ProjectReport),
            Endpoint("project_destroy", "/projects/{id}", "DELETE")
        ]

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def create(
        self,
        name: str,
        currency: str,
        leader_id: int,
        customer_id: int,
        deal_id: int = None,
        finish_date: datetime.date = None,
        identifier: str = None,
        billing_address: str = None,
        billing_email_to: str = None,
        billing_email_cc: str = None,
        billing_notes: str = None,
        setting_include_time_report: bool = None,
        billing_variant: ProjectBillingVariant = None,
        hourly_rate: float = None,
        budget: float = None,
        tags: list = None,
        custom_properties: dict = None,
        info: str = None,
        fixed_price: bool = False,
    ):
        """
        Create a new project.

        :param name: Name of the project
        :param currency: Currency used by the project (e.g. EUR)
        :param leader_id: User id of the project leader
        :param customer_id: Company id of the customer
        :param deal_id: Deal id the the project originated from
        :param finish_date: Finish date (default ``None``)
        :param identifier: Project Identifier (default ``None``)
        :param billing_address: Billing address the invoices go to (default ``None``)
        :param billing_email_to: Email address to send billing email to (default ``None``)
        :param billing_email_cc: Email address to cc in billing emails (default ``None``)
        :param billing_notes: Billing notes (default ``None``)
        :param setting_include_time_report: Include time report in billing emails (default ``None``)
        :param billing_variant: Billing variant used (default ``None``)
        :param hourly_rate: Hourly rate that will get billed (default ``None``)
        :param budget: Budget for the project (default ``None``)
        :param tags: Array of additional tags (default ``None``)
        :param custom_properties: Custom values used by the project (default ``None``)
        :param info: Additional information (default ``None``)
        :param fixed_price: If the project is a fixed price projects (default ``False``)

        :type name: str
        :type currency: str
        :type leader_id: int
        :type customer_id: int
        :type deal_id: int
        :type finish_date: datetime.date, str
        :type identifier: str
        :type billing_address: str
        :type billing_email_to: str
        :type billing_email_cc: str
        :type billing_notes: str
        :type setting_include_time_report: bool
        :type billing_variant: :class:`.ProjectBillingVariant`, str
        :type hourly_rate: float
        :type budget: float
        :type tags: list
        :type custom_properties: dict
        :type info: str
        :type fixed_price: bool

        :returns: The created project object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`

        .. note::
            The parameter ``identifier`` is required if number ranges are manual.

        .. note::
            If you create a project with ``fixed_price = True``, ``budget`` also has to be specified
        """
        data = {
            "name": name,
            "currency": currency,
            "leader_id": leader_id,
            "customer_id": customer_id
        }

        if fixed_price and budget is None:
            raise ValueError("When you create a fixed price project, the project budget must be set")

        for key, value in (
            ("deal_id", deal_id),
            ("finish_date", finish_date),
            ("identifier", identifier),
            ("billing_address", billing_address),
            ("billing_email_to", billing_email_to),
            ("billing_email_cc", billing_email_cc),
            ("billing_notes", billing_notes),
            ("setting_include_time_report", setting_include_time_report),
            ("billing_variant", billing_variant),
            ("hourly_rate", hourly_rate),
            ("budget", budget),
            ("tags", tags),
            ("custom_properties", custom_properties),
            ("info", info),
            ("fixed_price", fixed_price)
        ):
            if value is not None:
                if key in ["finish_date"] and isinstance(value, datetime.date):
                    data[key] = self._convert_date_to_iso(value)
                else:
                    data[key] = value

        return self._moco.post("project_create", data=data)

    def update(
        self,
        project_id: int,
        name: str = None,
        leader_id: int = None,
        customer_id: int = None,
        deal_id: int = None,
        finish_date: datetime.date = None,
        identifier: str = None,
        billing_address: str = None,
        billing_email_to: str = None,
        billing_email_cc: str = None,
        billing_notes: str = None,
        setting_include_time_report: bool = None,
        billing_variant: ProjectBillingVariant = None,
        hourly_rate: float = None,
        budget: float = None,
        tags: list = None,
        custom_properties: dict = None,
        info: str = None
    ):
        """
        Update an existing project.

        :param project_id: Id of the project to update
        :param name: Name of the project (default ``None``)
        :param leader_id: User id of the project leader (default ``None``)
        :param customer_id: Company id of the customer (default ``None``)
        :param deal_id: Deal id of the project (default ``None``)
        :param finish_date: Finish date (default ``None``)
        :param identifier: Project Identifier (default ``None``)
        :param billing_address: Address the invoices go to (default ``None``)
        :param billing_email_to: Email address to send billing emails to (default ``None``)
        :param billing_email_cc: Email address to cc in billing emails (default ``None``)
        :param billing_notes: Billing notes
        :param setting_include_time_report: Include time reports in billing emails
        :param billing_variant: Billing variant used (default ``None``)
        :param hourly_rate: Hourly rate that will get billed (default ``None``)
        :param budget: Budget for the project (default ``None``)
        :param tags: Array of additional tags (default ``None``)
        :param custom_properties: Custom values used by the project (default ``None``)
        :param info: Additional information (default ``None``)

        :type project_id: int
        :type name: str
        :type leader_id: int
        :type customer_id: int
        :type deal_id: int
        :type finish_date: datetime.date, str
        :type identifier: str
        :type billing_address: str
        :type billing_email_to: str
        :type billing_email_cc: str
        :type billing_notes: str
        :type setting_include_time_report: bool
        :type billing_variant: :class:`.ProjectBillingVariant`, str
        :type hourly_rate: float
        :type budget: float
        :type tags: list
        :type custom_properties: dict
        :type info: str

        :returns: The updated project object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "id": project_id
        }

        data = {}
        for key, value in (
            ("name", name),
            ("leader_id", leader_id),
            ("customer_id", customer_id),
            ("deal_id", deal_id),
            ("finish_date", finish_date),
            ("identifier", identifier),
            ("billing_address", billing_address),
            ("billing_email_to", billing_email_to),
            ("billing_email_cc", billing_email_cc),
            ("billing_notes", billing_notes),
            ("setting_include_time_report", setting_include_time_report),
            ("billing_variant", billing_variant),
            ("hourly_rate", hourly_rate),
            ("budget", budget),
            ("tags", tags),
            ("custom_properties", custom_properties),
            ("info", info)
        ):
            if value is not None:
                if key in ["finish_date"] and isinstance(value, datetime.date):
                    data[key] = self._convert_date_to_iso(value)
                else:
                    data[key] = value

        return self._moco.put("project_update", ep_params=ep_params, data=data)

    def get(
        self,
        project_id: int
    ):
        """
        Get a single project.

        :param project_id: Id of the project

        :type project_id: int

        :returns: Project object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "id": project_id
        }

        return self._moco.get("project_get", ep_params=ep_params)

    def getlist(
        self,
        include_archived: bool = None,
        include_company: bool = None,
        leader_id: int = None,
        company_id: int = None,
        created_from: datetime.date = None,
        created_to: datetime.date = None,
        updated_from: datetime.date = None,
        updated_to: datetime.date = None,
        tags: list = None,
        identifier: str = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Get a list of projects.

        :param include_archived: Include archived projects (default ``None``)
        :param include_company: Include the complete company object or just the company id (default ``None``)
        :param leader_id: User id of the project leader (default ``None``)
        :param company_id: Company id the projects are assigned to (default ``None``)
        :param created_from: Created start date (default ``None``)
        :param created_to: Created end date (default ``None``)
        :param updated_from: Updated start date (default ``None``)
        :param updated_to: Updated end date (default ``None``)
        :param tags: Array of tags (default ``None``)
        :param identifier: Project identifier (default ``None``)
        :param sort_by: Field to sort the results by (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type include_archived: bool
        :type include_company: bool
        :type leader_id: int
        :type company_id: int
        :type created_from: datetime.date, str
        :type created_to: datetime.date, str
        :type updated_from: datetime.date, str
        :type updated_to: datetime.date, str
        :type tags: list
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of project objects
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`
        """
        params = {}

        # all parameters that could be datetime.date objects we need to convert
        date_param_keys = [
            "created_from",
            "created_to",
            "updated_from",
            "updated_to"
        ]

        for key, value in (
            ("include_archived", include_archived),
            ("include_company", include_company),
            ("leader_id", leader_id),
            ("company_id", company_id),
            ("created_from", created_from),
            ("created_to", created_to),
            ("updated_from", updated_from),
            ("updated_to", updated_to),
            ("tags", tags),
            ("identifier", identifier),
            ("page", page),
        ):
            if value is not None:
                if key in date_param_keys and isinstance(value, datetime.date):
                    params[key] = self._convert_date_to_iso(value)
                else:
                    params[key] = value

        # add sort order if set
        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get("project_getlist", params=params)

    def assigned(
        self,
        active: bool = None,
    ):
        """
        Get list of all project currently assigned to the user.

        :param active: Show only active or inactive projects (default ``None``)

        :type active: bool

        :returns: List of project objects
        :rtype: :class:`moco_wrapper.util.response.ListResponse`
        """

        params = {}
        for key, value in (
            ("active", active),
        ):
            if value is not None:
                params[key] = value

        return self._moco.get("project_assigned", params=params)

    def archive(
        self,
        project_id: int
    ):
        """
        Archive a project.

        :param project_id: Id of the project to archive

        :type project_id: int

        :returns: The archived project
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "id": project_id
        }

        return self._moco.put("project_archive", ep_params=ep_params)

    def unarchive(
        self,
        project_id: int
    ):
        """
        Unarchive a project.

        :param project_id: Id of the project to unarchive

        :type project_id: int

        :returns: The unarchived project
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "id": project_id
        }

        return self._moco.put("project_unarchive", ep_params=ep_params)

    def report(
        self,
        project_id: int
    ):
        """
        Retrieve a project report.

        :param project_id: Id of the project

        :type project_id: int

        :returns: Report with the most important project business indicators
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`

        .. note::
            All costs are in the accounts main currency, it might differ from the budget and billable items.

        """
        ep_params = {
            "id": project_id
        }

        return self._moco.get("project_report", ep_params=ep_params)

    def destroy(
        self,
        project_id: int
    ):
        """
        Deletes a project. Only possible if there are no activities, invoices, offers or expenses

        :param project_id: Id of the project to delete

        :type project_id: int

        :returns: Empty response on success
        :rtype: :class:`moco_wrapper.util.response.EmptyResponse`

        .. note::
            Deleting a project is only possible if there are no acitivities, invoices offers or
            expenses
        """

        ep_params = {
            "id": project_id
        }

        return self._moco.get("project_destroy", ep_params=ep_params)
