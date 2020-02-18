from moco_wrapper.util.response import JsonResponse, ListingResponse, EmptyResponse
from moco_wrapper.util.generator import InvoiceItemGenerator

from .. import IntegrationTest
from datetime import date

class TestInvoicePayment(IntegrationTest):
    def get_customer(self):
        with self.recorder.use_cassette("TestInvoicePayment.get_customer"):
            customer_create = self.moco.Company.create(
                "TestInvoicePayment",
                company_type="customer"
            )
            return customer_create.data
    
    def get_invoice(self):
        customer = self.get_customer()

        with self.recorder.use_cassette("TestInvoicePayment.get_invoice"):
            gen = InvoiceItemGenerator()
            items = [
                gen.generate_title("dummy invoice item title"),
                gen.generate_description("dummy invoice item description"),
                gen.generate_lump_position("server hardware", 2000)
            ]
            
            invoice_create = self.moco.Invoice.create(
                customer.id,
                "dummy invoice",
                date(2020, 1, 1),
                date(2021, 1, 1),
                date(2020, 1, 1),
                date(2020, 3, 1),
                "dummy invoice",
                19,
                "EUR",
                items,
            )

            return invoice_create.data

    def test_getlist(self):
        invoice = self.get_invoice()
        
        with self.recorder.use_cassette("TestInvoicePayment.test_getlist"):
            payment_list = self.moco.InvoicePayment.getlist(invoice_id=invoice.id)

            assert payment_list.response.status_code == 200

            assert isinstance(payment_list, ListingResponse)


    