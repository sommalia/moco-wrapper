from moco_wrapper.util.response import JsonResponse, ListingResponse, EmptyResponse
from moco_wrapper.util.generator import InvoiceItemGenerator, InvoicePaymentGenerator

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

            assert payment_list.current_page == 1
            assert payment_list.is_last is not None
            assert payment_list.next_page is not None
            assert payment_list.total is not None
            assert payment_list.page_size is not None

    def test_create(self):
        invoice = self.get_invoice()

        with self.recorder.use_cassette("TestInvoicePayment.test_create"):
            payment_date = date(2020, 1, 2)
            amount = 200
            currency = "EUR"

            payment_create = self.moco.InvoicePayment.create(
                payment_date,
                invoice.id,
                amount,
                "EUR"
            )

            assert payment_create.response.status_code == 200

            assert isinstance(payment_create, JsonResponse)

            assert payment_create.data.date == payment_date.isoformat()
            assert payment_create.data.paid_total == amount
            assert payment_create.data.currency == currency
            assert payment_create.data.invoice.id == invoice.id 
    
    def test_create_bulk(self):
        invoice = self.get_invoice()

        with self.recorder.use_cassette("TestInvoicePayment.test_create_bulk"):
            gen = InvoicePaymentGenerator()
            items = [
                gen.generate(date(2020, 1, 1), invoice.id, 200, "EUR"),
                gen.generate(date(2020, 1, 2), invoice.id, 150, "EUR")
            ]

            payment_create = self.moco.InvoicePayment.create_bulk(items)

            assert payment_create.response.status_code == 200
            
            assert isinstance(payment_create, ListingResponse )

            assert payment_create.current_page == 1
            assert payment_create.is_last is not None
            assert payment_create.next_page is not None
            assert payment_create.total is not None
            assert payment_create.page_size is not None


    def test_get(self):
        invoice = self.get_invoice()

        with self.recorder.use_cassette("TestInvoicePayment.test_get"):
            payment_date = date(2020, 1, 2)
            amount = 200
            currency = "EUR"

            payment_create = self.moco.InvoicePayment.create(
                payment_date,
                invoice.id,
                amount,
                "EUR"
            )

            payment_get = self.moco.InvoicePayment.get(payment_create.data.id)

            assert payment_create.response.status_code == 200
            assert payment_get.response.status_code == 200

            assert isinstance(payment_create, JsonResponse)
            assert isinstance(payment_get, JsonResponse)

            assert payment_get.data.date == payment_date.isoformat()
            assert payment_get.data.paid_total == amount
            assert payment_get.data.currency == currency
            assert payment_get.data.invoice.id == invoice.id 

    def test_update(self):
        invoice = self.get_invoice()

        with self.recorder.use_cassette("TestInvoicePayment.test_update"):
            payment_date = date(2020, 1, 2)
            amount = 200
            currency = "EUR"

            payment_create = self.moco.InvoicePayment.create(
                date(2019, 12, 31),
                invoice.id,
                1,
                "EUR"
            )

            payment_update = self.moco.InvoicePayment.update(
                payment_create.data.id,
                payment_date=payment_date,
                paid_total=amount,
                currency="EUR"
            )

            assert payment_create.response.status_code == 200
            assert payment_update.response.status_code == 200

            assert isinstance(payment_create, JsonResponse)
            assert isinstance(payment_update, JsonResponse)

            assert payment_update.data.date == payment_date.isoformat()
            assert payment_update.data.paid_total == amount
            assert payment_update.data.currency == currency
            assert payment_update.data.invoice.id == invoice.id

    def test_delete(self):
        invoice = self.get_invoice()

        with self.recorder.use_cassette("TestInvoicePayment.test_delete"):
            payment_create = self.moco.InvoicePayment.create(
                date(2020, 1, 1),
                invoice.id,
                100,
                "EUR"
            )

            payment_delete = self.moco.InvoicePayment.delete(payment_create.data.id)

            assert payment_create.response.status_code == 200
            assert payment_delete.response.status_code == 204

            assert isinstance(payment_create, JsonResponse)
            assert isinstance(payment_delete, EmptyResponse)


    