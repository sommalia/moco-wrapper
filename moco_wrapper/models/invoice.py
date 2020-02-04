from .base import MWRAPBase
from ..const import API_PATH

from enum import Enum
from datetime import date

class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    CREATED = "created"
    SENT = "sent"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    OVERDUE = "overdue"
    IGNORED = "ignored"

class InvoiceChangeAddress(str, Enum):
    INVOICE = "invoice"
    PROJECT = "project"
    CUSTOMER = "customer"

class Invoice(MWRAPBase):
    """Models for handling invoices."""

    def __init__(self, moco):
        self._moco = moco

    def getlist(
        self,
        status: InvoiceStatus = None,
        date_from: date = None,
        date_to: date = None,
        tags: list = None,
        identifier: str = None,
        term: str = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
        ):
        """retrieve a list of invoices

        :param status: status the invoice has ("draft", "created", "sent", "partially_paid", "paid", "overdue", "ignored"), see InvoiceStatus
        :param date_from: filter starting date
        :param date_to: filter end date
        :param tags: list of tags
        :param identifier: identifier string (ex. R1903-003)
        :param term: wildcard search term withing title and identifier
        :param sort_by: field to sort results by
        :param sort_order: asc or desc (default asc)
        :param page: page number (default 1)
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
            ("page", page),
        ):
            
            if value is not None:
                if key in ["date_from", "date_to"] and isinstance(value, date):
                    params[key] = value.isoformat()
                elif key in ["tags"] and isinstance(value, list):
                    params[key] = ",".join(value)
                else:
                    params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["invoice_getlist"], params=params)
 
    def locked(
        self,
        status: InvoiceStatus = None,
        date_from: date = None,
        date_to: date = None,
        identifier: str = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
        ):        
        """retrieve a list of locked invoices

        :param status: status the invoice has ("draft", "created", "sent", "partially_paid", "paid", "overdue", "ignored"), see InvoiceStatus
        :param date_from: filter starting date
        :param date_to: filter end date
        :param identifier: identifier string (ex. R1903-003)
        :param sort_by: field to sort results by
        :param sort_order: asc or desc (default asc)
        :param page: page number (default 1)
        :returns: list of invoice objects
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
                if key in ["date_from", "date_to"] and isinstance(value, date):
                    params[key] = value.isoformat()
                else:
                    params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["invoice_locked"], params=params)


    def get(
        self,
        id: int
        ):
        """retrieve a single invoice

        :param id: invoice id
        :returns: single invoice
        """
        return self._moco.get(API_PATH["invoice_get"].format(id=id))

    def pdf(
        self,
        id: int
        ):
        """retrieve the invoice document as pdf 

        :param id: invoice id
        :returns: filestream of the invoice pdf file
        """
        return self._moco.get(API_PATH["invoice_get_doc"].format(id=id))

    def timesheet(
        self,
        id: int
        ):
        """retrieve the invoice timesheet document as pdf

        :param id: invoice id
        :return: filestream of the invoices timesheet document file
        """
        return self._moco.get(API_PATH["invoice_get_timesheet"].format(id=id))

    def update_status(
        self,
        id: int,
        status: InvoiceStatus
        ):
        """updates an invoices status

        :param id: invoice id
        :param status: new status of the invoice, see InvoiceStatus
        :returns: updated invoice object

        """
        data = {
            "status": status
        }

        return self._moco.put(API_PATH["invoice_update_status"].format(id=id), data=data)

    def create(
        self,
        customer_id: int,
        recipient_address: str,
        created_date: date,
        due_date: date,
        service_period_from: date,
        service_period_to: date,
        title: str,
        tax: float,
        currency: str,
        items: list,
        status: InvoiceStatus = InvoiceStatus.CREATED,
        change_address: InvoiceChangeAddress = InvoiceChangeAddress.INVOICE,
        salutation: str = None,
        footer: str= None,
        discount: float = None,
        cash_discount: float = None,
        cash_discount_days: int = None,
        project_id: int = None
        ):
        """creates a new invoice

        :param customer_id: id of the customer (see company)
        :param recipient_address: entry text for the customer (ex. "Dear my customer...")
        :param created_date: date the invoice was cerated (format YYYY-MM-DD)
        :param due_date: date the invoice is due (format YYYY-MM-DD)
        :param service_period_from: service period start date (format YYYY-MM-DD, ie "2018-08-01")
        :param service_period_to: service period end date (format YYYY-MM-DD, ie "2018-08-30")
        :param title: invoice title
        :param tax: tax percent (between 0.0 and 100.0)
        :param currency: a valid currency code of the accoutn (ex. EUR)
        :param items: invoice item (see InvoiceItemGenerator)
        :param status: status of the invoice ("created", "draft"), default is created
        :param change_address: address propagation ("invoice", "project", "customer"), default is "invoice", see InvoiceChangeAddress
        :param salutation: salutation text
        :param footer: footer text
        :param discount: discount in percent (between 0.0 and 100.0)
        :param cash_discount: cash discount in percent (between 0.0 and 100.0)
        :param cash_discount_days: how many days is the cash discount valid (ex. 4)
        :param project_id: id of the project the invoice belongs to
        :returns: the created invoice
        """
        data = {
            "customer_id" : customer_id,
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

        #overwrite all date fields in data with isoformat
        for date_key in ["date", "due_date", "service_period_from", "service_period_to"]:
            if isinstance(data[date_key], date):
                data[date_key] = data[date_key].isoformat()

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





    

