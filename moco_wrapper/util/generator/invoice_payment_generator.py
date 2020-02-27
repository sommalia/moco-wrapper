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
        """generates an invoice payment item that can be supplied to a bulk created

        :param payment_date: date of the payment
        :param invoice_id: id of the invoice the payment belongs to
        :param paid_total: amount that was paid (ex 200)
        :param currency: currency of the amout that was paid (ex. EUR)
        :returns: an invoice payment item



        use like this 

        .. code-block

        gen = InvoicePaymentGenerator()
        items = [gen.generate("2019-10-10", 1, 200, "EUR"), gen.generate("2020-04-04", 2, 540, "CHF")]
        moco.InvoicePayment.create_bulk(items)

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