import datetime
from typing import List

from moco_wrapper.util.endpoint import Endpoint
from moco_wrapper.models import objector_models as om
from moco_wrapper.models.base import MWRAPBase

from enum import Enum


class InvoiceStatus(str, Enum):
    """
    Enumeration for allowed values that can be supplied for the ``status`` argument of :meth:`.Invoice.getlist`,
    :meth:`.Invoice.update_status` and :meth:`.Invoice.create`.

    Example usage:

    .. code-block:: python

        from moco_wrapper.models.invoice import InvoiceStatus
        from moco_wrapper import Moco

        m = Moco()
        new_invoice = m.Invoice.create(
            ..
            status = InvoiceStatus.DRAFT
        )
    """
    DRAFT = "draft"
    CREATED = "created"
    SENT = "sent"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    OVERDUE = "overdue"
    IGNORED = "ignored"
    """
    .. warning::
        Do not use ``IGNORED`` for creating invoices, only updating and filtering.
    """


class InvoiceChangeAddress(str, Enum):
    """
    Enumeration for allowed values that can be supplied for ``change_address`` argument of :meth:`.Invoice.create`.

    .. code-block:: python

        from moco_wrapper.models.invoice import InvoiceChangeAddress
        from moco_wrapper import Moco

        m = Moco()
        new_invoice = m.Invoice.create(
            ..
            change_address = InvoiceChangeAddress.PROJECT
        )

    """
    INVOICE = "invoice"
    PROJECT = "project"
    CUSTOMER = "customer"


class Invoice(MWRAPBase):
    """
    Model for handling invoices.
    """

    @staticmethod
    def endpoints() -> List[Endpoint]:
        """
        Returns all endpoints associated with the model

        :returns: List of Endpoint objects
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`

        """
        return [
            Endpoint("invoice_create", "/invoices", "POST", om.Invoice),
            Endpoint("invoice_update", "/invoices/{id}", "PUT", om.Invoice),
            Endpoint("invoice_get", "/invoices/{id}", "GET", om.Invoice),
            Endpoint("invoice_getlist", "/invoices", "GET", om.Invoice),
            Endpoint("invoice_send_email", "/invoices/{id}/send_email", "POST", om.InvoiceEmail),
            Endpoint("invoice_update_status", "/invoices/{id}/update_status", "PUT", om.Invoice),
            Endpoint("invoice_locked", "/invoices/locked", "GET", om.Invoice),
            Endpoint("invoice_pdf", "/invoices/{id}.pdf", "GET"),
            Endpoint("invoice_timesheet_pdf", "/invoices/{id}/timesheet.pdf", "GET"),
            Endpoint("invoice_timesheet_activities", "/invoices/{id}/timesheet", "GET", om.Activity)
        ]

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def getlist(
        self,
        status: InvoiceStatus = None,
        date_from: datetime.date = None,
        date_to: datetime.date = None,
        tags: list = None,
        identifier: str = None,
        term: str = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Retrieve a list of invoices.

        :param status: State of the invoice (default ``None``)
        :param date_from: Starting date (default ``None``)
        :param date_to: End date (default ``None``)
        :param tags: List of tags (default ``None``)
        :param identifier: Identifier string (e.g. R1903-003) (default ``None``)
        :param term: Wildcard search term (default ``None``)
        :param sort_by: Field to sort results by (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type status: :class:`.InvoiceStatus`, str
        :type date_from: datetime.date, str
        :type date_to: datetime.date, str
        :type tags: list
        :type identifier: str
        :type term: str
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of invoice objects
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`
        """
        params = {}
        for key, value in (
            ("status", status),
            ("date_from", date_from),
            ("date_to", date_to),
            ("tags", tags),
            ("identifier", identifier),
            ("term", term),
            ("page", page),
        ):

            if value is not None:
                if key in ["date_from", "date_to"] and isinstance(value, datetime.date):
                    params[key] = self._convert_date_to_iso(value)
                elif key in ["tags"] and isinstance(value, list):
                    params[key] = ",".join(value)
                else:
                    params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get("invoice_getlist", params=params)

    def locked(
        self,
        status: InvoiceStatus = None,
        date_from: datetime.date = None,
        date_to: datetime.date = None,
        identifier: str = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Retrieve a list of locked invoices.

        :param status: State of the invoice (default ``None``)
        :param date_from: Start date (default ``None``)
        :param date_to: End date (default ``None``)
        :param identifier: Identifier string (ex. R1903-003) (default ``None``)
        :param sort_by: Field to sort results by (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type status: :class:`.InvoiceStatus`, str
        :type date_from: datetime.date, str
        :type date_to: datetime.date, str
        :type identifier: str
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of invoice objects
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`
        """
        params = {}
        for key, value in (
            ("status", status),
            ("date_from", date_from),
            ("date_to", date_to),
            ("identifier", identifier),
            ("page", page)
        ):
            if value is not None:
                if key in ["date_from", "date_to"] and isinstance(value, datetime.date):
                    params[key] = self._convert_date_to_iso(value)
                else:
                    params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get("invoice_locked", params=params)

    def get(
        self,
        invoice_id: int
    ):
        """
        Retrieve a single invoice.

        :param invoice_id: Invoice id

        :type invoice_id: int

        :returns: Single invoice object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "id": invoice_id,
        }

        return self._moco.get("invoice_get", ep_params=ep_params)

    def pdf(
        self,
        invoice_id: int
    ):
        """
        Retrieve the invoice document as pdf.

        :param invoice_id: Invoice id

        :type invoice_id: int

        :returns: Invoice pdf
        :rtype: :class:`moco_wrapper.util.response.FileResponse`
        """
        ep_params = {
            "id": invoice_id
        }

        return self._moco.get("invoice_pdf", ep_params=ep_params)

    def timesheet_pdf(
        self,
        invoice_id: int
    ):
        """
        Retrieve the invoice timesheet document as pdf.

        .. note::
            Invoices that have timesheets cannot be created over the api and must be created manually
            by billing unbilled tasks.

        :param invoice_id: Invoice id

        :type invoice_id: int

        :return: Invoice timesheet as pdf
        :rtype: :class:`moco_wrapper.util.response.FileResponse`
        """
        ep_params = {
            "id": invoice_id
        }

        return self._moco.get("invoice_timesheet_pdf", ep_params=ep_params)

    def timesheet_activities(
        self,
        invoice_id: int
    ):
        """
        Retrieve all activities that are associated with the given invoice

        .. note::
            Invoices that have timesheets cannot be created over the api and must be created manually
            by billing unbilled tasks.

        :param invoice_id: Invoice id
        :type invoice_id: int

        :return: List of activities
        :rtype: :class:`moco_wrapper.util.response.ListResponse`
        """
        ep_params = {
            "id": invoice_id
        }

        return self._moco.get("invoice_timesheet_activities", ep_params=ep_params)

    def update_status(
        self,
        invoice_id: int,
        status: InvoiceStatus
    ):
        """
        Updates the state of an invoices.

        :param invoice_id: Invoice id
        :param status: New state of the invoice

        :type invoice_id: int
        :type status: :class:`.InvoiceStatus`, str

        :return: Empty response on success
        :rtype: :class:`moco_wrapper.util.response.EmptyResponse`
        """
        ep_params = {
            "id": invoice_id
        }

        data = {
            "status": status
        }

        return self._moco.put("invoice_update_status", ep_params=ep_params, data=data)

    def create(
        self,
        customer_id: int,
        recipient_address: str,
        created_date: datetime.date,
        due_date: datetime.date,
        service_period_from: datetime.date,
        service_period_to: datetime.date,
        title: str,
        tax: float,
        currency: str,
        items: list,
        status: InvoiceStatus = InvoiceStatus.CREATED,
        change_address: InvoiceChangeAddress = InvoiceChangeAddress.INVOICE,
        salutation: str = None,
        footer: str = None,
        discount: float = None,
        cash_discount: float = None,
        cash_discount_days: int = None,
        project_id: int = None,
        tags: list = []
    ):
        """
        Creates a new invoice.

        :param customer_id: Id of the customer/company
        :param recipient_address: Customers address
        :param created_date: Creation date of the invoice
        :param due_date: Date the invoice is due
        :param service_period_from: Service period start date
        :param service_period_to: Service period end date
        :param title: Title of the invoice
        :param tax: Tax percent (between 0.0 and 100.0)
        :param currency: Currency code (e.g. EUR)
        :param items: Invoice items
        :param status: State of the invoice (default :attr:`.InvoiceStatus.CREATED`)
        :param change_address: Address propagation (default :attr:`.InvoiceChangeAddress.INVOICE`)
        :param salutation: Salutation text (default ``None``)
        :param footer: Footer text (default ``None``)
        :param discount: Discount in percent (between 0.0 and 100.0) (default ``None``)
        :param cash_discount: Cash discount in percent (between 0.0 and 100.0) (default ``None``)
        :param cash_discount_days: How many days is the cash discount valid (ex. 4) (default ``None``)
        :param project_id: Id of the project the invoice belongs to (default ``None``)
        :param tags: List of tags (default ``[]``)

        :type customer_id: int
        :type recipient_address: str
        :type created_date: datetime.date, str
        :type due_date: datetime.date, str
        :type service_period_from: datetime.date, str
        :type service_period_to: datetime.date, str
        :type title: str
        :type tax: float
        :type currency: str
        :type items: list
        :type status: :class:`.InvoiceStatus`, str
        :type change_address: :class:`.InvoiceChangeAddress`, str
        :type salutation: str
        :type footer: str
        :type discount: float
        :type cash_discount: float
        :type cash_discount_days: float
        :type project_id: int
        :type tags: list

        :returns: The created invoice
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`

        .. note::
            Note that if you create an invoice with a project, that project must also belong to the customer the invoice
            was created for.

        .. seealso::

            :class:`moco_wrapper.util.generator.InvoiceItemGenerator`

        """
        data = {
            "customer_id": customer_id,
            "recipient_address": recipient_address,
            "date": created_date,
            "due_date": due_date,
            "service_period_from": service_period_from,
            "service_period_to": service_period_to,
            "title": title,
            "tax": tax,
            "currency": currency,
            "items": items,
        }

        # overwrite all date fields in data with isoformat
        for date_key in ["date", "due_date", "service_period_from", "service_period_to"]:
            if isinstance(data[date_key], datetime.date):
                data[date_key] = self._convert_date_to_iso(data[date_key])

        for key, value in (
            ("status", status),
            ("change_address", change_address),
            ("salutation", salutation),
            ("footer", footer),
            ("discount", discount),
            ("cash_discount", cash_discount),
            ("cash_discount_days", cash_discount_days),
            ("project_id", project_id),
            ("tags", tags)
        ):
            if value is not None:
                data[key] = value

        return self._moco.post("invoice_create", data=data)

    def send_email(
        self,
        invoice_id: int,
        emails_to: str,
        subject: str,
        text: str,
        emails_cc: str = None,
        emails_bcc: str = None
    ):
        """
        Send an invoice by mail

        :param invoice_id: Id of the invoice to send
        :param emails_to: Target email address (or a list of multiple email addresses)
        :param subject: Email subject
        :param text: Email text
        :param emails_cc: Email address for cc (or a list of multiple email addresses) (default ``None``)
        :param emails_bcc: Email address for bcc (or a list of multiple email addresses) (default ``None``)

        :type invoice_id: int
        :type emails_to: str, list
        :type subject: str
        :type text: str
        :type emails_cc: str, list
        :type emails_bcc: str, list

        :returns: Object containing the details of the sent mail
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`

        .. note::

            If you want to send an email to the default recipient configured in the project or customer,
            set ``emails_to`` and ``emails_cc`` To ``None``.

        """
        ep_params = {
            "id": invoice_id
        }

        if emails_to is None:
            emails_to = []

        if emails_cc is None:
            emails_cc = []

        if emails_bcc is None:
            emails_bcc = []

        data = {
            "subject": subject,
            "text": text
        }

        if isinstance(emails_to, list):
            data["emails_to"] = ";".join(emails_to)
        else:
            data["emails_to"] = emails_to

        for key, value in (
            ("emails_cc", emails_cc),
            ("emails_bcc", emails_bcc)
        ):

            if value is not None:
                if key in ["emails_cc", "emails_bcc"] and isinstance(value, list) and len(value) > 0:
                    data[key] = ";".join(value)
                elif isinstance(value, list) and len(value) == 0:
                    # skip lists with 0 elements
                    pass
                else:
                    data[key] = value

        return self._moco.post("invoice_send_email", ep_params=ep_params, data=data)
