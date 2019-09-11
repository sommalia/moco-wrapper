from ..const import API_PATH
from .base import MocoBase

class Invoice(MocoBase):
    """Models for handling invoices."""

    def __init__(self, moco):
        self._moco = moco

    def getlist(
        self,
        status = None,
        date_from = None,
        date_to = None,
        tags = None,
        identifier = None,
        term = None,
        sort_by = None,
        sort_order = 'asc'
        ):
        """retrieve a list of invoices

        :param status: status the invoice has ("draft", "created", "sent", "partially_paid", "paid", "overdue", "ignored")
        :param date_from: filter starting date (format YYYY-MM-DD)
        :param date_to: filter end date (format YYYY-MM-DD)
        :param tags: list of tags
        :param identifier: identifier string (ex. R1903-003)
        :param term: wildcard search term withing title and identifier
        :param sort_by: field to sort results by
        :param sort_order: asc or desc
        :returns: list of invoice objects
        """
        params = {}
        for key, value in (
            ("status", status),
            ("date_from", date_from),
            ("date_to", date_to),
            ("tags", tags),
            ("identifier", identifier),
            ("term", term),
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["invoice_getlist"], params=params)
 
    def locked(
        self,
        status = None,
        date_from = None,
        date_to = None,
        tags = None,
        identifier = None,
        term = None,
        sort_by = None,
        sort_order = 'asc'
        ):        
        """retrieve a list of locked invoices

        :param status: status the invoice has ("draft", "created", "sent", "partially_paid", "paid", "overdue", "ignored")
        :param date_from: filter starting date (format YYYY-MM-DD)
        :param date_to: filter end date (format YYYY-MM-DD)
        :param tags: list of tags
        :param identifier: identifier string (ex. R1903-003)
        :param sort_by: field to sort results by
        :param sort_order: asc or desc
        :returns: list of invoice objects
        """
        params = {}
        for key, value in (
            ("status", status),
            ("date_from", date_from),
            ("date_to", date_to),
            ("tags", tags),
            ("identifier", identifier),
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["invoice_locked"], params=params)


    def get(
        self,
        id
        ):
        """retrieve a single invoice

        :param id: invoice id
        :returns: single invoice
        """
        return self._moco.get(API_PATH["invoice_get"].format(id=id))

    def get_doc(
        self,
        id
        ):
        """retrieve the invoice document

        :param id: invoice id
        :returns: filestream of the invoice pdf file
        """
        return self._moco.get(API_PATH["invoice_get_doc"].format(id=id))

    def get_timesheet(
        self,
        id
        ):
        """retrieve the invoice timesheet document

        :param id: invoice id
        :return: filestream of the invoices timesheet document file
        """
        return self._moco.get(API_PATH["invoice_get_timesheet"].format(id=id))

    def update_status(
        self,
        id,
        status
        ):
        """updates an invoices status

        :param id: invoice id
        :param status: new status of the invoice
        :returns: updated invoice object

        """
        data = {
            "status": status
        }

        return self._moco.put(API_PATH["invoice_update_status"].format(id=id), data=data)

    def create(
        self,
        customer_id,
        recipient_address,
        date,
        due_date,
        service_period,
        title ,
        tax,
        currency,
        items,
        status = 'created',
        change_address = 'invoice',
        salutation = None,
        footer = None,
        discount = None,
        cash_discount = None,
        cash_discount_days = None,
        project_id = None
        ):
        """creates a new invoice

        :param customer_id: id of the customer (see company)
        :param recipient_address: entry text for the customer (ex. "Dear my customer...")
        :param date: date if the invoice (format YYYY-MM-DD)
        :param due_date: date the invoice is due (format YYYY-MM-DD)
        :param service_period: service period (ex. "Aug 18")
        :param title: invoice title
        :param tax: tax percent
        :param currency: a valid currency code of the accoutn (ex. EUR)
        :param items: invoice item (see InvoiceItemGenerator)
        :param status: status of the invoice ("created", "draft"), default is created
        :param change_address: address propagation ("invoice", "project", "customer"), default is "invoice"
        :param salutation: salutation text
        :param footer: footer text
        :param discount: discount in percent
        :param cash_discount: cash discount in percent
        :param cash_discount_days: how many days is the cash discount valid (ex. 4)
        :param project_id: id of the project the invoice belongs to
        :returns: the created invoice
        """
        data = {
            "customer_id" : customer_id,
            "recipient_address": recipient_address,
            "date": date,
            "due_date": due_date,
            "service_period": service_period,
            "title": title,
            "tax": tax,
            "currency": currency,
            "items": items,
        }

        for key, value in (
            ("status", status),
            ("change_address", change_address),
            ("salutation", salutation),
            ("footer", footer),
            ("discount", discount),
            ("cash_discount", cash_discount),
            ("cash_discount_days", cash_discount_days),
            ("project_id", project_id)
        ):
            if value is not None:
                data[key] = value

        return self._moco.post(API_PATH["invoice_create"], data=data)





    

