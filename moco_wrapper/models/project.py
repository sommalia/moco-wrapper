import datetime

from moco_wrapper.models.base import MWRAPBase  
from moco_wrapper.const import API_PATH

from enum import Enum

class ProjectBillingVariant(str, Enum):
    """
    Enumeration for allowed values of the ``billing_variant`` argument of :meth:`.Project.create` and :meth:`.Project.update`.

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
        finish_date: datetime.date = None,
        identifier: str = None,
        billing_address: str = None,
        billing_variant: ProjectBillingVariant = None,
        hourly_rate: float = None,
        budget: float = None,
        labels: list = None,
        custom_properties: dict = None,
        info: str = None
        ):
        """
        Create a new project.

        :param name: Name of the project
        :param currency: Currency used by the project (e.g. EUR)
        :param leader_id: User id of the project leader
        :param customer_id: Company id of the customer
        :param finish_date: Finish date
        :param identifier: Project Identifier
        :param billing_address: Billing adress the invoices go to
        :param billing_variant: Billing variant used. For allowed values see :class:`.ProjectBillingVariant`.
        :param hourly_rate: Hourly rate that will get billed 
        :param budget: Budget for the project
        :param labels: Array of additional labels
        :param custom_properties: Custom values used by the project
        :param info: Additional information
        :returns: The created project object

        .. note::

            The parameter ``identifier`` is required if number ranges are manual.
        """
        data = {
            "name": name,
            "currency" : currency,
            "leader_id": leader_id,
            "customer_id": customer_id
        }


        for key, value in (
            ("finish_date", finish_date),
            ("identifier", identifier),
            ("billing_address", billing_address),
            ("billing_variant", billing_variant),
            ("hourly_rate", hourly_rate),
            ("budget", budget),
            ("labels", labels),
            ("custom_properties", custom_properties),
            ("info", info)
        ):
            if value is not None:
                if key in ["finish_date"] and isinstance(value, datetime.date):
                    data[key] = self._convert_date_to_iso(value)
                else:
                    data[key] = value
                
        return self._moco.post(API_PATH["project_create"], data=data)

    def update(
        self,
        id: int,
        name: str = None,
        leader_id: int = None,
        customer_id: int = None,
        finish_date: datetime.date = None,
        identifier: str = None,
        billing_address: str = None,
        billing_variant: ProjectBillingVariant = None,
        hourly_rate: float = None,
        budget: float = None,
        labels: list = None,
        custom_properties: dict = None,
        info: str = None
        ):
        """
        Update an existing project.

        :param id: Id of the project to update
        :param name: Name of the project
        :param leader_id: User id of the project leader
        :param customer_id: Company id of the customer
        :param finish_date: Finish date
        :param identifier: Project Identifier
        :param billing_address: Address the invoices go to
        :param billing_variant: Billing variant used. For allowed values see :class:`.ProjectBillingVariant`.
        :param hourly_rate: Hourly rate that will get billed 
        :param budget: Budget for the project
        :param labels: Array of additional labels
        :param custom_properties: Custom values used by the project
        :param info: Additional information
        :returns: The updated project object
        """

        data = {}
        for key, value in (
            ("name", name),
            ("leader_id", leader_id),
            ("customer_id", customer_id),
            ("finish_date", finish_date),
            ("identifier", identifier),
            ("billing_address", billing_address),
            ("billing_variant", billing_variant),
            ("hourly_rate", hourly_rate),
            ("budget", budget),
            ("labels", labels),
            ("custom_properties", custom_properties),
            ("info", info)
        ):
            if value is not None:
                if key in ["finish_date"] and isinstance(value, datetime.date):
                    data[key] = self._convert_date_to_iso(value)
                else:
                    data[key] = value

        return self._moco.put(API_PATH["project_update"].format(id=id), data=data)

    def get(
        self,
        id: int
        ):
        """
        Get a single project.

        :param id: Id of the project
        :returns: Project object
        """

        return self._moco.get(API_PATH["project_get"].format(id=id))

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

        :param include_archived: Include archived projects
        :param include_company: Include the complete company object or just the company id
        :param leader_id: User id of the project leader
        :param company_id: Company id the projects are assigned to
        :param created_from: Created start date 
        :param created_to: Created end date
        :param updated_from: Updated start date
        :param updated_to: Updated end date
        :param tags: Array of tags
        :param identifier: Project identifer
        :param sort_by: Field to sort the results by
        :param sort_order: asc or desc (default asc)
        :param page: Page number (default 1)
        :returns: List of project objects
        """

        params = {}
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
                if key in ["created_from", "created_to", "updated_from", "updated_to" ] and isinstance(value, datetime.date):
                    params[key] = self._convert_date_to_iso(value)
                else:
                    params[key] = value

        #add sort order if set
        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)


        return self._moco.get(API_PATH["project_getlist"], params=params)

    def assigned(
        self,
        active: bool = None,
        sort_by: str = None,
        sort_order: str = 'asc', 
        page: int = 1
        ):
        """
        Get list of all project currently assigned to the user.

        :param active: Show only active or inacitve projects
        :param sort_by: Sort by field
        :param sort_order: asc or desc (default asc)
        :param page: Page number (default 1)
        :returns: List of project objects
        """

        params = {}
        for key, value in (
            ("active", active),
            ("page", page),
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["project_assigned"], params=params)

    def archive(
        self,
        id: int
        ):
        """
        Archive a project.

        :param id: Id of the project to archive
        :returns: The archived project
        """
        return self._moco.put(API_PATH["project_archive"].format(id=id))

    def unarchive(
        self,
        id: int
        ):
        """
        Unarchive a project.

        :param id: Id of the project to unarchive
        :returns: The unarchived project
        """
        return self._moco.put(API_PATH["project_unarchive"].format(id=id))

    def report(
        self,
        id: int
        ):
        """
        Retrieve a project report.

        All costs are in the accounts main currency, it might differ from the budget and billable items.

        :param id: Id of the project
        :returns: Report with the most important project business indicators
        """
        return self._moco.get(API_PATH["project_report"].format(id=id))    

    
    