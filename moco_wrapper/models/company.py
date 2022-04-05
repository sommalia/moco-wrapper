from typing import List

from moco_wrapper.util.endpoint import Endpoint
from moco_wrapper.models import objector_models as om
from moco_wrapper.models.base import MWRAPBase

from enum import Enum


class CompanyType(str, Enum):
    """
    Enumeration of the type of companies that exist. Can be used to supply the ``company_type`` argument of
    :meth:`.Company.create`, :meth:`.Company.update` and :meth:`.Company.getlist`

    Example Usage:

    .. code-block:: python

        from moco_wrapper import Moco
        from moco_wrapper.models.company import CompanyType

        m = Moco()
        new_supplier = m.Company.create(
            ..
            company_type = CompanyType.ORGANIZATION
        )
    """
    CUSTOMER = "customer"
    SUPPLIER = "supplier"
    ORGANIZATION = "organization"


class Company(MWRAPBase):
    """
    Class for handling companies.

    Companies come in three different flavours (see :class:`.CompanyType`), customers are companies you do stuff for
    and send invoices to. suppliers are companies that supply stuff to you as a customer. Finally organizations are
    companies that do not fit the label customer or supplier. For the most part you will interact with companies of
    type customer.

    Example usage:

    .. code-block:: python

        from moco_wrapper import Moco

        m = Moco()
        new_customer = m.Company.create(
            "my new customer",
            "customer"
        )

    """

    @staticmethod
    def endpoints() -> List[Endpoint]:
        """
        Returns all endpoints associated with the model

        :returns: List of Endpoint objects
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`

        """
        return [
            Endpoint("company_create", "/companies", "POST", om.Company),
            Endpoint("company_update", "/companies/{id}", "PUT", om.Company),
            Endpoint("company_get", "/companies/{id}", "GET", om.Company),
            Endpoint("company_getlist", "/companies", "GET", om.Company)
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
        company_type: CompanyType,
        website: str = None,
        fax: str = None,
        phone: str = None,
        email: str = None,
        billing_email_cc: str = None,
        address: str = None,
        info: str = None,
        custom_properties: dict = None,
        tags: list = None,
        user_id: int = None,
        currency: str = None,
        identifier: str = None,
        billing_tax: float = None,
        default_invoice_due_days: int = None,
        country_code: str = None,
        vat_identifier: str = None,
        iban: str = None,
        debit_number: int = None,
        credit_number: int = None,
        footer: str = None
    ):
        """
        Create a company.

        :param name: Name of the company
        :param company_type: Either customer, supplier or organization
        :param website: Url of the companies website (default ``None``)
        :param fax: Fax number of the company (default ``None``)
        :param phone: Phone number of the company (default ``None``)
        :param email: Email address of the company (default ``None``)
        :param billing_email_cc: Email address to cc for billing emails (default ``None``)
        :param address: Company address (default ``None``)
        :param info: Additional information about the company (default ``None``)
        :param custom_properties: Custom properties dictionary (default ``None``)
        :param tags: Array of tags (default ``None``)
        :param user_id: User Id of the responsible person (default ``None``)
        :param currency: Currency the company uses (only customer) (default ``None``)
        :param identifier: Identifier of the company
            (only mandatory when not automatically assigned) (default ``None``)
        :param billing_tax: Billing tax value (from 0 to 100) (default ``None``)
        :param default_invoice_due_days: Payment target days for the company when creating invoices
            (only customer) (default ``None``)
        :param country_code: ISO Alpha-2 Country Code like "DE" / "CH" / "AT" in upper case -
            default is account country (default ``None``)
        :param vat_identifier: Vat identifier for eu companies (default ``None``)
        :param iban: Iban number (only supplier) (default ``None``)
        :param debit_number: Debit number (if bookkeeping is enabled) (only customer) (default ``None``)
        :param credit_number: Credit number (if bookkeeping is enabled) (only supplier) (default ``None``)
        :param footer: Some html (appears at the end of invoices) (default ``None``)

        :type name: str
        :type company_type: :class:`.CompanyType`, str
        :type website: str
        :type fax: str
        :type phone: str
        :type email: str
        :type billing_email_cc: str
        :type address: str
        :type info: str
        :type custom_properties: dict
        :type tags: list
        :type user_id: int
        :type currency: str
        :type identifier: str
        :type billing_tax: float
        :type default_invoice_due_days: int
        :type country_code: str
        :type vat_identifier: str
        :type iban: str
        :type debit_number: int
        :type credit_number: int
        :type footer: str

        :returns: The created company
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`

        .. note::

            When supplying a vat_identifier, make sure it is valid

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
            ("billing_email_cc", billing_email_cc),
            ("address", address),
            ("info", info),
            ("custom_properties", custom_properties),
            ("tags", tags),
            ("user_id", user_id),
            ("country_code", country_code),
            ("vat_identifier", vat_identifier),
            ("footer", footer)
        ):
            if value is not None:
                data[key] = value

        # set company specific parameters
        if company_type == CompanyType.SUPPLIER:
            for key, value in (
                ("iban", iban),
                ("credit_number", credit_number)
            ):
                if value is not None:
                    data[key] = value

        if company_type == CompanyType.CUSTOMER:
            for key, value in (
                ("currency", currency),
                ("identifier", identifier),
                ("billing_tax", billing_tax),
                ("invoice_due_days", default_invoice_due_days),
                ("debit_number", debit_number)
            ):
                if value is not None:
                    data[key] = value

        return self._moco.post("company_create", data=data)

    def update(
        self,
        company_id: int,
        company_type: CompanyType = None,
        name: str = None,
        website: str = None,
        fax: str = None,
        phone: str = None,
        email: str = None,
        billing_email_cc: str = None,
        address: str = None,
        info: str = None,
        custom_properties: dict = None,
        tags: list = None,
        user_id: int = None,
        currency: str = None,
        identifier: str = None,
        billing_tax: float = None,
        default_invoice_due_days: int = None,
        country_code: str = None,
        vat_identifier: str = None,
        iban: str = None,
        debit_number: int = None,
        credit_number: int = None,
        footer: str = None,
    ):
        """
        Update a company.

        :param company_id: Id of the company
        :param company_type: Type of the company to modify (default ``None``)
        :param name: Name of the company (default ``None``)
        :param website: Url of the companies website (default ``None``)
        :param fax: Fax number of the company (default ``None``)
        :param phone: Phone number of the company (default ``None``)
        :param email: Email address of the company (default ``None``)
        :param billing_email_cc: Email address to cc in billing emails (default ``None``)
        :param address: Company address (default ``None``)
        :param info: Additional information about the company (default ``None``)
        :param custom_properties: Custom properties dictionary (default ``None``)
        :param tags: Array of tags (default ``None``)
        :param user_id: Id of the responsible person (default ``None``)
        :param currency: Currency the company uses (only customer) (default ``None``)
        :param identifier: Identifier of the company (only mandatory when not automatically assigned)
            (only customer) (default ``None``)
        :param billing_tax: Billing tax value (only customer) (default ``None``)
        :param default_invoice_due_days: payment target days for the company when creating invoices
            (only customer) (default ``None``)
        :param country_code: ISO Alpha-2 Country Code like "DE" / "CH" / "AT" in upper case -
            default is account country (default ``None``)
        :param vat_identifier: vat identifier for eu companies (default ``None``)
        :param iban: iban number (only supplier) (default ``None``)
        :param debit_number: Debit number (if bookkeeping is enabled) (only customer) (default ``None``)
        :param credit_number: Credit number (if bookkeeping is enabled) (ony supplier) (default ``None``)

        :type company_id: int
        :type name: str
        :type company_type: :class:`.CompanyType`, str
        :type website: str
        :type fax: str
        :type phone: str
        :type email: str
        :type billing_email_cc: str
        :type address: str
        :type info: str
        :type custom_properties: dict
        :type tags: list
        :type user_id: int
        :type currency: str
        :type identifier: str
        :type billing_tax: float
        :type default_invoice_due_days: int
        :type country_code: str
        :type vat_identifier: str
        :type iban: str
        :type debit_number: int
        :type credit_number: int
        :type footer: str

        :returns: The updated company
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "id": company_id
        }

        data = {}

        for key, value in (
            ("type", company_type),
            ("name", name),
            ("website", website),
            ("fax", fax),
            ("phone", phone),
            ("email", email),
            ("billing_email_cc", billing_email_cc),
            ("address", address),
            ("info", info),
            ("custom_properties", custom_properties),
            ("tags", tags),
            ("user_id", user_id),
            ("currency", currency),
            ("identifier", identifier),
            ("billing_tax", billing_tax),
            ("invoice_due_days", default_invoice_due_days),
            ("country_code", country_code),
            ("vat_identifier", vat_identifier),
            ("iban", iban),
            ("debit_number", debit_number),
            ("credit_number", credit_number),
            ("footer", footer)
        ):
            if value is not None:
                data[key] = value

        return self._moco.put("company_update", ep_params=ep_params, data=data)

    def get(
        self,
        company_id: int
    ):
        """
        Get a single company.

        :param company_id: Id of the company

        :type company_id: int

        :returns: Single company object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "id": company_id
        }

        return self._moco.get("company_get", ep_params=ep_params)

    def getlist(
        self,
        company_type: CompanyType = None,
        tags: list = None,
        identifier: str = None,
        term: str = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Get a list of company objects.

        :param company_type: Type of company to filter for (default ``None``)
        :param term: Term to search for (default ``None``)
        :param tags: List of tags (default ``None``)
        :param identifier: Company identifier (default ``None``)
        :param sort_by: Field to sort by (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: page number (default ``1``)

        :type company_type: :class:`.CompanyType`, str
        :type tags: list
        :type identifier: str
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of companies
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`
        """

        params = {}
        for key, value in (
            ("type", company_type),
            ("tags", tags),
            ("identifier", identifier),
            ("term", term),
            ("page", page)
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get("company_getlist", params=params)
