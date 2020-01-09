from .base import MWRAPBase  
from ..const import API_PATH

from enum import Enum
from datetime import date

class ProjectBillingVariant(str, Enum):
    PROJECT = "project"
    TASK = "task"
    USER = "user"

class ProjectCurrency(str, Enum):
    EUR = "EUR"

class Project(MWRAPBase):
    """Class for handling projects."""

    def __init__(self, moco):
        self._moco = moco

    def create(
        self,
        name: str,
        currency: ProjectCurrency,
        finish_date: date,
        leader_id: int,
        customer_id: int,
        identifier: str = None,
        billing_address: str = None,
        billing_variant: ProjectBillingVariant = None,
        hourly_rate: float = None,
        budget: float = None,
        labels: list = None,
        custom_properties: dict = None,
        info: str = None
        ):
        """create a new project

        :param name: name of the project
        :param currency: currency of the project (EUR) (use project.ProjectCurrency)
        :param finish_date: finish date formatted YYYY-MM-DD
        :param leader_id: user id of the project leader
        :param customer_id: company id of the customer
        :param identifier: project identifier is only mandatory if number ranges are manual
        :param billing_address: billing adress the invoices go to
        :param billing_variant: "project", "task" or "user" (default is project) (use project.ProjectBillingVariant)
        :param hourly_rate: hourly rate that will get billed 
        :param budget: budget for the project
        :param labels: array of additional labels
        :param custom_properties: custom values used by the project
        :param info: additional information
        :returns: the created project object
        """
        data = {
            "name": name,
            "currency" : currency,
            "leader_id": leader_id,
            "customer_id": customer_id
        }

    
        if isinstance(finish_date, date):
            data["finish_date"] = finish_date.isoformat()
        else:
            data["finish_date"] = finish_date


        for key, value in (
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
                data[key] = value

        return self._moco.post(API_PATH["project_create"], data=data)

    def update(
        self,
        id: int,
        name: str = None,
        finish_date: date = None,
        leader_id: int = None,
        customer_id: int = None,
        identifier: str = None,
        billing_address: str = None,
        billing_variant: ProjectBillingVariant = None,
        hourly_rate: float = None,
        budget: float = None,
        labels: list = None,
        custom_properties: dict = None,
        info: str = None
        ):
        """updates an existing project

        :param id: id of the project to update
        :param name: name of the project
        :param finish_date: finish date formatted YYYY-MM-DD
        :param leader_id: user id of the project leader
        :param customer_id: company id of the customer
        :param identifier: only mandatory if number ranges are manual
        :param billing_address: adress the invoices go to
        :param billing_variant: project, task or user (default is project)
        :param hourly_rate: hourly rate that will get billed 
        :param budget: budget for the project
        :param labels: array of additional labels
        :param custom_properties: custom values used by the project
        :param info: additional information
        :returns: the updated project object
        """

        data = {}
        for key, value in (
            ("name", name),
            ("finish_date", finish_date),
            ("leader_id", leader_id),
            ("customer_id", customer_id),
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
                if key == "finish_date" and isinstance(value, date):
                    data[key] = value.isoformat()
                else:
                    data[key] = value

        return self._moco.put(API_PATH["project_update"].format(id=id), data=data)

    def get(
        self,
        id: int
        ):
        """get a single project

        :param id: id of the project
        :returns: project object
        """

        return self._moco.get(API_PATH["project_get"].format(id=id))

    def getlist(
        self,
        include_archived: bool = None,
        include_company: bool = None,
        leader_id: int = None,
        company_id: int = None,
        created_from: date = None,
        created_to: date = None,
        updated_from: date = None,
        updated_to: date = None,
        tags: list = None,
        identifier: str = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
        ):
        """Get a list of projects

        :param include_archived: true/false include archived projects
        :param include_company: true/false include the whole company or just the id
        :param leader_id: user id of the project leader
        :param company_id: company id the projects are assigned to
        :param created_from: created start date (format YYYY-MM-DD)
        :param created_to: created end date (format YYYY-MM-DD)
        :param updated_from: updated start date (format YYYY-MM-DD)
        :param updated_to: updated end date (format YYYY-MM-DD)
        :param tags: array of tags
        :param identifier: project identifer
        :param sort_by: field to sort the results by
        :param sort_order: asc or desc (default asc)
        :param page: page number (default 1)
        :returns: list of project objects
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
                if key in ["created_from", "created_to", "updated_from", "updated_to" ] and isinstance(value, date):
                    params[key] = value.isoformat()
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
        """get list of all project currently assigned to the user 

        :param active: true/false show only active or inacitve projects
        :param sort_by: sort by field
        :param sort_order: asc or desc (default asc)
        :param page: page number (default 1)
        :returns: list of project objects
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
        """archive a project

        :param id: id of the project to archive
        """
        return self._moco.put(API_PATH["project_archive"].format(id=id))

    def unarchive(
        self,
        id: int
        ):
        """unarchive a project

        :param id: id of the project to unarchive
        """
        return self._moco.put(API_PATH["project_unarchive"].format(id=id))

    def report(
        self,
        id: int
        ):
        """retrieve a project report

        all cost are in the accounts main currency, it might differ from the budget and billable items

        :param id: id of the project
        :returns: report with the most important project business indicators
        """
        return self._moco.get(API_PATH["project_report"].format(id=id))    

    
    