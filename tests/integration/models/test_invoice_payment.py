from moco_wrapper.util.response import ObjectResponse, ListResponse, PagedListResponse, EmptyResponse
from moco_wrapper.util.generator import InvoiceItemGenerator, InvoicePaymentGenerator
from moco_wrapper.models.company import CompanyType

from .. import IntegrationTest
from datetime import date


class TestInvoicePayment(IntegrationTest):
    def get_customer(self):
        with self.recorder.use_cassette("TestInvoicePayment.get_customer"):
            customer_create = self.moco.Company.create(
                name="TestInvoicePayment.get_customer",
                company_type=CompanyType.CUSTOMER
            )
            return customer_create.data

    def get_invoice(self):
        customer = self.get_customer()

        with self.recorder.use_cassette("TestInvoicePayment.get_invoice"):
            gen = InvoiceItemGenerator()
            items = [
                gen.generate_title(
                    title="dummy invoice item title"
                ),
                gen.generate_description(
                    description="dummy invoice item description"
                ),
                gen.generate_lump_position(
                    title="server hardware",
                    net_total=2000
                )
            ]

            invoice_create = self.moco.Invoice.create(
                customer_id=customer.id,
                recipient_address="MY customer dummy address",
                created_date=date(2020, 1, 1),
                due_date=date(2021, 1, 1),
                service_period_from=date(2020, 1, 1),
                service_period_to=date(2020, 3, 1),
                title="TestInvoicePayment.get_invoice",
                tax=19,
                currency="EUR",
                items=items,
            )

            return invoice_create.data

    def test_getlist(self):
        invoice = self.get_invoice()

        with self.recorder.use_cassette("TestInvoicePayment.test_getlist"):
            payment_list = self.moco.InvoicePayment.getlist(
                invoice_id=invoice.id
            )

            assert payment_list.response.status_code == 200

            assert type(payment_list) is PagedListResponse

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
                payment_date=payment_date,
                invoice_id=invoice.id,
                paid_total=amount,
                currency="EUR"
            )

            assert payment_create.response.status_code == 200

            assert type(payment_create) is ObjectResponse

            assert payment_create.data.date == payment_date.isoformat()
            assert payment_create.data.paid_total == amount
            assert payment_create.data.currency == currency
            assert payment_create.data.invoice.id == invoice.id

    def test_create_bulk(self):
        invoice = self.get_invoice()

        with self.recorder.use_cassette("TestInvoicePayment.test_create_bulk"):
            gen = InvoicePaymentGenerator()
            items = [
                gen.generate(
                    payment_date=date(2020, 1, 1),
                    invoice_id=invoice.id,
                    paid_total=200,
                    currency="EUR"
                ),
                gen.generate(
                    payment_date=date(2020, 1, 2),
                    invoice_id=invoice.id,
                    paid_total=150,
                    currency="EUR"
                )
            ]

            payment_create = self.moco.InvoicePayment.create_bulk(items)

            assert payment_create.response.status_code == 200

            assert type(payment_create) is ListResponse

    def test_get(self):
        invoice = self.get_invoice()

        with self.recorder.use_cassette("TestInvoicePayment.test_get"):
            payment_date = date(2020, 1, 2)
            amount = 200
            currency = "EUR"

            payment_create = self.moco.InvoicePayment.create(
                payment_date=payment_date,
                invoice_id=invoice.id,
                paid_total=amount,
                currency="EUR"
            )

            payment_get = self.moco.InvoicePayment.get(
                payment_id=payment_create.data.id
            )

            assert payment_create.response.status_code == 200
            assert payment_get.response.status_code == 200

            assert type(payment_create) is ObjectResponse
            assert type(payment_get) is ObjectResponse

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
                payment_date=date(2019, 12, 31),
                invoice_id=invoice.id,
                paid_total=1,
                currency="EUR"
            )

            payment_update = self.moco.InvoicePayment.update(
                payment_id=payment_create.data.id,
                payment_date=payment_date,
                paid_total=amount,
                currency="EUR"
            )

            assert payment_create.response.status_code == 200
            assert payment_update.response.status_code == 200

            assert type(payment_create) is ObjectResponse
            assert type(payment_update) is ObjectResponse

            assert payment_update.data.date == payment_date.isoformat()
            assert payment_update.data.paid_total == amount
            assert payment_update.data.currency == currency
            assert payment_update.data.invoice.id == invoice.id

    def test_delete(self):
        invoice = self.get_invoice()

        with self.recorder.use_cassette("TestInvoicePayment.test_delete"):
            payment_create = self.moco.InvoicePayment.create(
                payment_date=date(2020, 1, 1),
                invoice_id=invoice.id,
                paid_total=100,
                currency="EUR"
            )

            payment_delete = self.moco.InvoicePayment.delete(
                payment_id=payment_create.data.id
            )

            assert payment_create.response.status_code == 200
            assert payment_delete.response.status_code == 204

            assert type(payment_create) is ObjectResponse
            assert type(payment_delete) is EmptyResponse
