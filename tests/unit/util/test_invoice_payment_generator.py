from moco_wrapper.util.generator import InvoicePaymentGenerator

class TestInvoicePaymentGenerator(object):

    def setup(self):
        self.generator = InvoicePaymentGenerator()

    def test_generate(self):
        payment_date = '2019-10-10'
        invoice_id = 5
        paid_total = 200
        currency = "EUR"

        data = self.generator.generate(payment_date, invoice_id, paid_total, currency)

        assert data["date"] == payment_date
        assert data["invoice_id"] == invoice_id
        assert data["paid_total"] == paid_total
        assert data["currency"] == currency