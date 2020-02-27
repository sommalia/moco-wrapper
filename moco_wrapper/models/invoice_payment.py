import datetime

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH

class InvoicePayment(MWRAPBase):
    """
    Class for handling invoice payments.
    """

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def getlist(
        self,
        invoice_id: int = None,
        date_from: datetime.date = None,
        date_to: datetime.date = None,
        sort_by: str = None,
        sort_order = 'asc',
        page = 1
        ):
        """
        Retrieve a list of invoice payments.

        :param invoice_id: Id of a corresponding invoice
        :param date_from: Start date
        :param date_to: End date
        :param sort_by: Field to sort results by
        :param sort_order: asc or desc (default asc)
        :param page: Page number (default 1)
        :returns: List of invoice payments
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
                    params[key] = self.convert_date_to_iso(value)
                else:
                    params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)


        return self._moco.get(API_PATH["invoice_payment_getlist"], params=params)

    def get(
        self,
        id: int
        ):
        """
        Retrieve a single invoice payment.

        :param id: Invoice payment id
        :returns: Single invoice payment object
        """
        return self._moco.get(API_PATH["invoice_payment_get"].format(id=id))

    def create(
        self,
        payment_date: datetime.date,
        invoice_id: int,
        paid_total: float,
        currency: str
        ):
        """
        Create a new invoice payment.

        :param payment_date: Date of the payment
        :param invoice_id: Id of the invoice this payment belongs to
        :param paid_total: Amount that was paid (ex. 193.50)
        :param currency: Currency used (e.g. EUR)
        :returns: The created invoice payment object
        """
        data = {
            "date": payment_date,
            "invoice_id": invoice_id,
            "paid_total": paid_total,
            "currency": currency
        }

        if isinstance(payment_date, datetime.date):
            data["date"] = self.convert_date_to_iso(payment_date)

        return self._moco.post(API_PATH["invoice_payment_create"], data=data)

    def create_bulk(
        self,
        items: list = []
        ):
        """
        Create multiple new invoice payments.

        :param items: Payment items
        :returns: List of created invoice payments

        .. seealso:: 
            :class:`moco_wrapper.util.generator.InvoicePaymentGenerator`

        Bulk creation if invoice payments items with generator:

        .. code-block:: python

            from moco_wrapper.util.generator import InvoicePaymentGenerator()
            from moco_wrapper import Moco

            items = [
                gen.generate(..),
                gen.generate(..)
            ]

            m = Moco()

            created_payments = m.InvoicePayment.create_bulk(items)

        """
        data = {
            "bulk_data": items
        }

        return self._moco.post(API_PATH["invoice_payment_create_bulk"], data=data)

    def update(
        self,
        id: int,
        payment_date: datetime.date = None,
        paid_total: float = None,
        currency: str= None
        ):
        """
        Updates an existing invoice payment.

        :param id: Id of the payment to update
        :param payment_date: Date of the payment
        :param paid_total: Amount that was paid
        :param currency: Currency (e.g. EUR)
        :returns: The updated invoice payment object
        """
        data = {}
        for key, value in (
            ("date", payment_date),
            ("paid_total", paid_total),
            ("currency", currency),
        ):
            if value is not None:
                if key in ["date"] and isinstance(value, datetime.date):
                    data[key] = self.convert_date_to_iso(value)
                else:
                    data[key] = value

        return self._moco.put(API_PATH["invoice_payment_update"].format(id=id), data=data)

    def delete(
        self,
        id: int
        ):
        """
        Deletes an invoice payment.

        :param id: Id of the payment to delete
        :returns: Empty response on success
        """
        return self._moco.delete(API_PATH["invoice_payment_delete"].format(id=id))
