from .base import MWRAPBase
from ..const import API_PATH

from enum import Enum

class CompanyType(str, Enum):
    CUSTOMER = "customer",
    SUPPLIER = "supplier",
    ORGANIZATION = "organization"

class CompanyCurrency(str, Enum):
    EUR = "EUR"

class Company(MWRAPBase):
    """Class for handling companies/customers"""


    def __init__(self, moco):
        """Initialize a company instance

        :param moco: An instance of :class Moco

        """
        self._moco = moco

    def create(
        self,
        name: str,
        company_type: CompanyType,
        website = None,
        fax = None,
        phone = None,
        email = None,
        address = None,
        info = None,
        custom_properties = None,
        labels = None,
        user_id = None,
        currency = None,
        identifier = None,
        billing_tax = None,
        default_invoice_due_days = None,
        country_code = None,
        ):
        """Create a company

        :param name: Name of the company
        :param company_type: Either customer, supplier or organization
        :param website: Url of the companies website
        :param fax: Fax number of the company
        :param phone: Phone number of the company
        :param email: Email address of the company
        :param info: Additional information about the company
        :param custom_properties: Custom properties dictionary
        :param labels: Array of labels
        :param user_id: Id of the responsible person
        :param currency: Currency the company uses (only mandatory when type == customer)
        :param identifer: Identifier of the company (only mandatory when not automatily assigned)
        :param billing_tax: Billing tax value (from 0 to 100)
        :param default_invoice_due_days: payment target days for the company when creating invoices
        :param country_code: ISO Alpha-2 Country Code like "DE" / "CH" / "AT" in upper case - default is account country
        """

        data = {
            "name": name,
            "type": company_type,
        }


        for key, value in (
            ("website", website),
            ("fax", fax),
            ("phone", phone),
            ("email", email),
            ("address", address),
            ("info", info),
            ("custom_properties", custom_properties),
            ("labels", labels),
            ("user_id", user_id),
            ("currency", currency),
            ("identifier", identifier),
            ("billing_tax", billing_tax),
            ("invoice_due_days", default_invoice_due_days),
            ("country_code", country_code)
        ):
            if value is not None:
                data[key] = value

        return self._moco.post(API_PATH["company_create"], data=data)

    def update(
        self,
        id,
        company_type: CompanyType = None,
        name = None,
        website = None,
        fax = None,
        phone = None,
        email = None,
        address = None,
        info = None,
        custom_properties = None,
        labels = None,
        user_id = None,
        currency = None,
        identifier = None,
        billing_tax = None,
        default_invoice_due_days = None,
        country_code = None
        ):
        """update a company

        :param id: Id of the company
        :param company_type: Type of the company to modify
        :param name: Name of the company
        :param website: Url of the companies website
        :param fax: Fax number of the company
        :param phone: Phone number of the company
        :param email: Email address of the company
        :param info: Additional information about the company
        :param custom_properties: Custom properties dictionary
        :param labels: Array of labels
        :param user_id: Id of the responsible person
        :param currency: Currency the company uses (only mandatory when type == customer)
        :param identifer: Identifier of the company (only mandatory when not automatily assigned)
        :param billing_tax: Billing tax value 
        :param default_invoice_due_days: payment target days for the company when creating invoices
        :param country_code: ISO Alpha-2 Country Code like "DE" / "CH" / "AT" in upper case - default is account country
        """
        data = {
  
        }


        for key, value in (
            ("type", company_type),
            ("name", name),
            ("website", website),
            ("fax", fax),
            ("phone", phone),
            ("email", email),
            ("address", address),
            ("info", info),
            ("custom_properties", custom_properties),
            ("labels", labels),
            ("user_id", user_id),
            ("currency", currency),
            ("identifier", identifier),
            ("billing_tax", billing_tax),
            ("invoice_due_days", default_invoice_due_days),
            ("country_code", country_code)
        ):
            if value is not None:
                data[key] = value

        return self._moco.put(API_PATH["company_update"].format(id=id), data=data)

    def get(
        self, 
        id
        ):
        """Get a single company by its id

        :param id: Id of the company
        :returns: single company object
        """
        return self._moco.get(API_PATH["company_get"].format(id=id))

    def getlist(
        self,
        company_type = None,
        tags = None,
        identifier = None,
        sort_by = None,
        sort_order = 'asc',
        page = 1
        ):
        """Get a list of company objects
        
        :param company_type: either "customer", "supplier", "organization"
        :param tags: list of tags
        :param identifier: company identifer
        :param sort_by: field to sort by
        :param sort_order: asc or desc
        :param page: page number (default 1)
        :returns: list of companyies
        """

        params = {}
        for key, value in (
            ("type", company_type),
            ("tags", tags),
            ("identifier", identifier),
            ("page", page)
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["company_getlist"], params=params)
        