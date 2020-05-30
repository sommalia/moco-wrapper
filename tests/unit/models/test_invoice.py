from moco_wrapper.util.generator import InvoiceItemGenerator

from .. import UnitTest
import pytest

from datetime import date


class TestInvoice(UnitTest):
    def test_create(self):
        generator = InvoiceItemGenerator()

        customer_id = 123456
        recipient_address = "My customer..."
        create_date = "2018-09-17"
        due_date = "2018-10-16"
        service_period_from = date(2019, 10, 1)
        service_period_to = date(2019, 10, 31)
        title = "Invoice"
        tax = 8.0
        currency = "CHF"
        items = [generator.generate_title("this is the title"), generator.generate_separator()]
        status = "created"
        change_address = "customer"
        salutation = "salute"
        footer = "footer text"
        discount = 10
        cash_discount = 2.5
        cash_discount_days = 5
        project_id = 654321
        tags = ["Hosting", "Europe"]

        response = self.moco.Invoice.create(
            customer_id,
            recipient_address,
            create_date,
            due_date,
            service_period_from,
            service_period_to,
            title,
            tax,
            currency,
            items,
            status=status,
            change_address=change_address,
            salutation=salutation,
            footer=footer,
            discount=discount,
            cash_discount=cash_discount,
            cash_discount_days=cash_discount_days,
            project_id=project_id,
            tags=tags
        )
        data = response["data"]

        assert data["customer_id"] == customer_id
        assert data["recipient_address"] == recipient_address
        assert data["date"] == create_date
        assert data["due_date"] == due_date
        assert data["service_period_from"] == service_period_from.isoformat()
        assert data["service_period_to"] == service_period_to.isoformat()
        assert data["title"] == title
        assert data["tax"] == tax
        assert data["currency"] == currency
        assert data["items"] == items

        assert data["status"] == status
        assert data["change_address"] == change_address

        assert data["salutation"] == salutation
        assert data["footer"] == footer
        assert data["discount"] == discount
        assert data["cash_discount"] == cash_discount
        assert data["cash_discount_days"] == cash_discount_days
        assert data["project_id"] == project_id
        assert data["tags"] == tags

        assert response["method"] == "POST"

    def test_create_default_status(self):
        generator = InvoiceItemGenerator()

        default_status = 'created'

        customer_id = 123456
        recipient_address = "My customer..."
        created_date = "2018-09-17"
        due_date = "2018-10-16"
        service_period_from = date(2019, 10, 1)
        service_period_to = date(2019, 10, 31)
        title = "Invoice"
        tax = 8.0
        currency = "CHF"
        items = [generator.generate_title("this is the title"), generator.generate_separator()]

        response = self.moco.Invoice.create(customer_id, recipient_address, created_date, due_date, service_period_from,
                                            service_period_to, title, tax, currency, items)
        data = response["data"]

        assert data["status"] == default_status

    def test_create_default_change_address(self):
        generator = InvoiceItemGenerator()

        default_change_address = 'invoice'

        customer_id = 123456
        recipient_address = "My customer..."
        created_date = "2018-09-17"
        due_date = "2018-10-16"
        service_period_from = date(2019, 10, 1)
        service_period_to = date(2019, 10, 31)
        title = "Invoice"
        tax = 8.0
        currency = "CHF"
        items = [generator.generate_title("this is the title"), generator.generate_separator()]

        response = self.moco.Invoice.create(customer_id, recipient_address, created_date, due_date, service_period_from,
                                            service_period_to, title, tax, currency, items)
        data = response["data"]

        assert data["change_address"] == default_change_address

    def test_update_status(self):
        invoice_id = 2
        status = "paid"

        response = self.moco.Invoice.update_status(invoice_id, status)
        data = response["data"]

        assert data["status"] == status
        assert response["method"] == "PUT"

    def test_timesheet(self):
        invoice_id = 2

        response = self.moco.Invoice.timesheet(invoice_id)

        assert response["method"] == "GET"

    def test_pdf(self):
        invoice_id = 2

        response = self.moco.Invoice.pdf(invoice_id)

        assert response["method"] == "GET"

    def test_get(self):
        invoice_id = 2

        response = self.moco.Invoice.get(invoice_id)

        assert response["method"] == "GET"

    def test_locked(self):
        status = "created"
        date_from = '2019-10-10'
        date_to = '2020-10-10'
        identifier = "INVOICE-001"

        response = self.moco.Invoice.locked(status=status, date_from=date_from, date_to=date_to, identifier=identifier)
        params = response["params"]

        assert params["status"] == status
        assert params["date_from"] == date_from
        assert params["date_to"] == date_to
        assert params["identifier"] == identifier

        assert response["method"] == "GET"

    def test_locked_sort_default(self):
        sort_by = "this is the field to sort by"

        response = self.moco.Invoice.locked(sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_locked_sort_overwrite(self):
        sort_by = "this is the field to sort by"
        sort_order = "desc"

        response = self.moco.Invoice.locked(sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_locked_page_default(self):
        page_default = 1

        response = self.moco.Invoice.locked()
        assert response["params"]["page"] == page_default

    def test_locked_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.Invoice.locked(page=page_overwrite)
        assert response["params"]["page"] == page_overwrite

    def test_getlist(self):
        status = "created"
        date_from = '2019-10-10'
        date_to = '2020-10-10'
        tags = ["these", "are", "the", "tags"]
        identifier = "INVOICE-001"
        term = "horse"

        response = self.moco.Invoice.getlist(status=status, date_from=date_from, date_to=date_to, tags=tags,
                                             identifier=identifier, term=term)
        params = response["params"]

        assert params["status"] == status
        assert params["date_from"] == date_from
        assert params["date_to"] == date_to
        assert params["tags"] == ",".join(tags)
        assert params["identifier"] == identifier
        assert params["term"] == term
        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        sort_by = "this is the field to sort by"

        response = self.moco.Invoice.getlist(sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "this is the field to sort by"
        sort_order = "desc"

        response = self.moco.Invoice.getlist(sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        page_default = 1

        response = self.moco.Invoice.getlist()
        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.Invoice.getlist(page=page_overwrite)
        assert response["params"]["page"] == page_overwrite
