class InvoicePaymentGenerator(object):
    
    def generate(
        self,
        date, 
        invoice_id,
        paid_total,
        currency
        ):
        """generates an invoice payment item that can be supplied to a bulk created

        :param date: date of the payment (format YYYY-MM-DD)
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

        return {
            "date": date,
            "invoice_id": invoice_id,
            "paid_total": paid_total,
            "currency" : currency,
        }