from .base import MWRAPBase
from ..const import API_PATH

from datetime import date

class InvoicePayment(MWRAPBase):
    """class for handling invoice payments(in german "rechnungen")."""
    def __init__(self, moco):
        self._moco = moco

    def getlist(
        self,
        invoice_id: int = None,
        date_from: date = None,
        date_to: date = None,
        sort_by = None,
        sort_order = 'asc',
        page = 1
        ):
        """retrieve all invoice payments

        :param invoice_id: Id of a corresponding invoice
        :param date_from: starting filter date
        :param date_to: end filter date
        :param sort_by: field to sort results by
        :param sort_order: asc or desc (default asc)
        :param page: page number (default 1)
        :returns: list of invoice payments
        """


        params = {}
        for key, value in (
            ("invoice_id", invoice_id),
            ("date_from", date_from),
            ("date_to", date_to),
            ("page", page),
        ):
            if value is not None:
                if key in ["date_from", "date_to"] and isinstance(value, date):
                    params[key] = value.isoformat()
                else:
                    params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)


        return self._moco.get(API_PATH["invoice_payment_getlist"], params=params)

    def get(
        self,
        id
        ):
        """retrieve a single payment

        :param id: payment id
        :returns: single payment object
        """
        return self._moco.get(API_PATH["invoice_payment_get"].format(id=id))

    def create(
        self,
        date,
        invoice_id,
        paid_total,
        currency
        ):
        """create a new payment

        :param date: date of the payment (format YYYY-MM-DD)
        :param invoice_id: id of the invoice this payment belongs to
        :param paid_total: amount that was paid (ex. 2000)
        :param currency: currency of the amount that was paid (ex. EUR)
        :returns: the created payment object
        """
        data = {
            "date": date,
            "invoice_id": invoice_id,
            "paid_total": paid_total,
            "currency": currency
        }

        return self._moco.post(API_PATH["invoice_payment_create"], data=data)

    def create_bulk(
        self,
        items = []
        ):
        """create multiple new payments

        :param items: payment items (field are the same as in the create method. Also see InvoicePaymentGenerator::generate()
        :returns: the created payments
        """
        data = {
            "bulk_data": items
        }

        return self._moco.post(API_PATH["invoice_payment_create_bulk"], data=data)

    def update(
        self,
        id,
        date = None,
        paid_total = None,
        currency = None
        ):
        """updates an existing payment

        :param id: id of the payment to update
        :param date: date of the payment (format YYYY-MM-DD)
        :param paid_total: amount that was paid
        :param currency: currency of the payment (ex. EUR)
        :returns: the updated payment object
        """
        data = {}
        for key, value in (
            ("date", date),
            ("paid_total", paid_total),
            ("currency", currency),
        ):
            if value is not None:
                data[key] = value

        return self._moco.put(API_PATH["invoice_payment_update"].format(id=id), data=data)

    def delete(
        self,
        id
        ):
        """deletes a payment

        :param id: id of the payment to delete
        """
        return self._moco.delete(API_PATH["invoice_payment_delete"].format(id=id))
