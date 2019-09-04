from .base import MocoBase
from ..const import API_PATH

class Company(MocoBase):
    """Class for handling companies"""


    def __init__(self, moco):
        """Initialize a company instance

        :param moco: An instance of :class Moco

        """
        self._moco = moco

    def create(
        self,
        name = None,
        company_type = None,
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
        default_invoice_due_days = None
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
        :param billing_tax: Billing tax value 
        :param default_invoice_due_days: Default payment target days for the company when creating invoices
        """

        data = {
            "name": name,
            "type": company_type,
        }

        if(company_type == "customer"):
            data["currency"] = currency

        #make check for all required arguments here
        #TODO

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
            ("default_invoice_due_days", default_invoice_due_days)
        ):
            if value is not None:
                data[key] = value;

        return self._moco.post(API_PATH["company_create"], data=data)

    def update(
        self,
        id,
        name = None,
        company_type = None,
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
        default_invoice_due_days = None
        ):
        """Update a company

        :param id: Id of the company
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
        :param billing_tax: Billing tax value 
        :param default_invoice_due_days: Default payment target days for the company when creating invoices
        """
        data = {}
        for key, value in (
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
            ("default_invoice_due_days", default_invoice_due_days)
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
        identifer = None
        ):
        """Get a list of company objects
        
        :param company_type: either "customer", "supplier", "organization"
        :param tags: list of tags
        :param identifer: company identifer
        :returns: list of companyies
        """

        params = {}
        for key, value in (
            ("type", company_type),
            ("tags", tags),
            ("identifer", identifer)
        ):
            if value is not None:
                params[key] = value

        return self._moco.get(API_PATH["company_getlist"], params=params)

    def delete(
        self,
        id
        ):
        """Deleting a company over the api is not possible for now"""
        pass

        