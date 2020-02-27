import datetime

from .base import BaseGenerator

class InvoicePaymentGenerator(BaseGenerator):
    
    def generate(
        self,
        payment_date: datetime.date, 
        invoice_id: int,
        paid_total: float,
        currency: str
        ):
        """
        Generates an invoice payment item that can be supplied to a bulk created

        :param payment_date: date of the payment
        :param invoice_id: id of the invoice the payment belongs to
        :param paid_total: amount that was paid (ex 200)
        :param currency: currency of the amout that was paid (ex. EUR)
        :returns: an invoice payment item

        Example usage

        .. code-block:: python

            from moco_wrapper.util.generator import InvoicePaymentGenerator
            from moco_wrapper import Moco
            from datetime import date

            m = Moco()
            gen = InvoicePaymentGenerator()

            items = [
                gen.generate(
                    "2019-10-10", 
                    1, 
                    200, 
                    "EUR"
                ), 
                gen.generate(
                    "2020-04-04", 
                    2, 
                    540, 
                    "CHF"
                ),
                gen.generate(
                    date(2020, 1, 1)
                    1,
                    300,
                    "EUR"
                )
            ]

            created_invoice_payment = m.InvoicePayment.create_bulk(items)

        .. seealso::

            :meth:`moco_wrapper.models.InvoicePayment.create_bulk`
        ..
        """

        item = {
            "date": payment_date,
            "invoice_id": invoice_id,
            "paid_total": paid_total,
            "currency" : currency,
        }

        for date_key in ["date"]:
            if isinstance(item[date_key], datetime.date):
                item[date_key] = self.convert_date_to_iso(item[date_key])

        return item