from .. import IntegrationTest

from datetime import date

from moco_wrapper.util.response import JsonResponse, ListingResponse, EmptyResponse, FileResponse, ErrorResponse
from moco_wrapper.util.generator import InvoiceItemGenerator
from moco_wrapper.models.invoice import InvoiceStatus, InvoiceChangeAddress
from moco_wrapper.models.company import CompanyType



class TestInvoice(IntegrationTest):
    def get_customer(self):
        with self.recorder.use_cassette("TestInvoice.get_customer"):
            customer_create = self.moco.Company.create(
                "TestInvoice",
                company_type="customer"
            )

            return customer_create.data

    def get_user(self):
        with self.recorder.use_cassette("TestInvoice.get_user"):
            user = self.moco.User.getlist().items[0]
            return user

    def get_project(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestInvoice.get_project"):
            project_create = self.moco.Project.create(
                "TestInvoice",
                "EUR",
                user.id,
                customer.id,
                finish_date=date(2020, 1, 1),
            )

            return project_create.data

    def test_getlist(self):
        with self.recorder.use_cassette("TestInvoice.test_getlist"):
            inv_getlist = self.moco.Invoice.getlist()

            assert inv_getlist.response.status_code == 200

            assert isinstance(inv_getlist, ListingResponse)

    def test_locked(self):
        with self.recorder.use_cassette("TestInvoice.test_locked"):
            inv_locked = self.moco.Invoice.locked()

            assert inv_locked.response.status_code == 200
            
            assert isinstance(inv_locked, ListingResponse)

    def test_get(self):
        customer = self.get_customer()

        with self.recorder.use_cassette("TestInvoice.test_get"):
            recipient_address = "Mein Kunde\nHauptstrasse 1\n8000 Zürich"
            creation_date = date(2018, 9, 17)
            due_date = date(2018, 10, 16)
            title = "invoice"
            tax = 8.0
            currency = "EUR"
            service_from_date = date(2019, 12, 1)
            service_to_date = date(2019, 12, 31)

            item_generator = InvoiceItemGenerator()
            items = [
                item_generator.generate_title("Hours"),
                item_generator.generate_description("Listing of all hours"),
                item_generator.generate_item("Service", quantity=2, unit="hours", unit_price=65, net_total=130)
            ]

            inv_create = self.moco.Invoice.create(
                customer.id, 
                recipient_address, 
                creation_date, 
                due_date, 
                service_from_date, 
                service_to_date, 
                title, 
                tax, 
                currency, 
                items
            )

            inv_get = self.moco.Invoice.get(inv_create.data.id)


            assert inv_create.response.status_code == 200
            assert inv_get.response.status_code == 200

            assert isinstance(inv_get, JsonResponse)
            assert isinstance(inv_create, JsonResponse)

            assert inv_get.data.customer_id == customer.id
            assert inv_get.data.title == title
            assert inv_get.data.date == creation_date.isoformat()
            assert inv_get.data.recipient_address == recipient_address
            assert inv_get.data.currency == currency
            assert inv_get.data.due_date == due_date.isoformat()

    def test_pdf(self):
        customer = self.get_customer()

        with self.recorder.use_cassette("TestInvoice.test_pdf"):
            recipient_address = "Mein Kunde\nHauptstrasse 1\n8000 Zürich"
            creation_date = date(2018, 9, 17)
            due_date = date(2018, 10, 16)
            title = "invoice"
            tax = 8.0
            currency = "EUR"
            service_from_date = date(2019, 12, 1)
            service_to_date = date(2019, 12, 31)

            item_generator = InvoiceItemGenerator()
            items = [
                item_generator.generate_title("Hours"),
                item_generator.generate_description("Listing of all hours"),
                item_generator.generate_item("Service", quantity=2, unit="hours", unit_price=65, net_total=130)
            ]

            inv_create = self.moco.Invoice.create(
                customer.id, 
                recipient_address, 
                creation_date, 
                due_date, 
                service_from_date, 
                service_to_date, 
                title, 
                tax, 
                currency, 
                items
            )

            inv_pdf = self.moco.Invoice.pdf(inv_create.data.id)

            assert inv_create.response.status_code == 200
            assert inv_pdf.response.status_code == 200

            assert isinstance(inv_create, JsonResponse)
            assert isinstance(inv_pdf, FileResponse)

    def test_timesheet_no_hours(self):
        customer = self.get_customer()
        
        with self.recorder.use_cassette("TestInvoice.test_timesheet_no_hours"):
            recipient_address = "Mein Kunde\nHauptstrasse 1\n8000 Zürich"
            creation_date = date(2018, 9, 17)
            due_date = date(2018, 10, 16)
            title = "invoice"
            tax = 8.0
            currency = "EUR"
            service_from_date = date(2019, 12, 1)
            service_to_date = date(2019, 12, 31)

            item_generator = InvoiceItemGenerator()
            items = [
                item_generator.generate_title("Hours"),
                item_generator.generate_description("Listing of all hours"),
                item_generator.generate_item("Service", quantity=2, unit="hours", unit_price=65, net_total=130)
            ]

            inv_create = self.moco.Invoice.create(
                customer.id,
                recipient_address, 
                creation_date, 
                due_date, 
                service_from_date, 
                service_to_date, 
                title, 
                tax, 
                currency,
                items
            )

            inv_time = self.moco.Invoice.timesheet(inv_create.data.id)
            
            assert inv_create.response.status_code == 200
            assert inv_time.response.status_code == 404

            assert isinstance(inv_create, JsonResponse)
            assert isinstance(inv_time, ErrorResponse)

    def test_update_status(self):
        customer = self.get_customer()

        with self.recorder.use_cassette("TestInvoice.test_update_status"):
            recipient_address = "Mein Kunde\nHauptstrasse 1\n8000 Zürich"
            creation_date = date(2018, 9, 17)
            due_date = date(2018, 10, 16)
            title = "invoice"
            tax = 8.0
            currency = "EUR"
            service_from_date = date(2019, 12, 1)
            service_to_date = date(2019, 12, 31)

            item_generator = InvoiceItemGenerator()
            items = [
                item_generator.generate_title("Hours"),
                item_generator.generate_description("Listing of all hours"),
                item_generator.generate_item("Service", quantity=2, unit="hours", unit_price=65, net_total=130)
            ]

            inv_create = self.moco.Invoice.create(
                customer.id, 
                recipient_address, 
                creation_date, 
                due_date, 
                service_from_date, 
                service_to_date, 
                title, 
                tax, 
                currency, 
                items
            )
            
            inv_update = self.moco.Invoice.update_status(
                inv_create.data.id, 
                InvoiceStatus.IGNORED
            )

            inv_get = self.moco.Invoice.get(inv_create.data.id)

            assert inv_create.response.status_code == 200
            assert inv_update.response.status_code == 204
            assert inv_get.response.status_code == 200

            assert isinstance(inv_create, JsonResponse)
            assert isinstance(inv_update, EmptyResponse)
            assert isinstance(inv_get, JsonResponse)

            assert inv_create.data.status == InvoiceStatus.CREATED
            assert inv_get.data.status == InvoiceStatus.IGNORED
            

    def test_create(self):
        customer = self.get_customer()

        with self.recorder.use_cassette("TestInvoice.test_create"):
            recipient_address = "Mein Kunde\nHauptstrasse 1\n8000 Zürich"
            creation_date = date(2018, 9, 17)
            due_date = date(2018, 10, 16)
            title = "invoice"
            tax = 8.0
            currency = "EUR"
            service_from_date = date(2019, 12, 1)
            service_to_date = date(2019, 12, 31)

            item_generator = InvoiceItemGenerator()
            items = [
                item_generator.generate_title("Hours"),
                item_generator.generate_description("Listing of all hours"),
                item_generator.generate_item("Service", quantity=2, unit="hours", unit_price=65, net_total=130)
            ]

            inv_create = self.moco.Invoice.create(
                customer.id, 
                recipient_address, 
                creation_date, 
                due_date, 
                service_from_date, 
                service_to_date, 
                title, 
                tax, 
                currency, 
                items
            )
            
            assert inv_create.response.status_code == 200

            assert isinstance(inv_create, JsonResponse)

            assert inv_create.data.title == "invoice"
            assert inv_create.data.currency == "EUR"
            assert inv_create.data.customer_id == customer.id
            assert inv_create.data.service_period_from == service_from_date.isoformat()
            assert inv_create.data.service_period_to == service_to_date.isoformat()
            assert inv_create.data.date == creation_date.isoformat()
            assert inv_create.data.due_date == due_date.isoformat()
            assert inv_create.data.recipient_address == recipient_address
            assert inv_create.data.tax == tax

    def test_create_with_project(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestInvoice.test_create_with_project"):
            recipient_address = "Mein Kunde\nHauptstrasse 1\n8000 Zürich"
            creation_date = date(2018, 9, 17)
            due_date = date(2018, 10, 16)
            title = "invoice"
            tax = 8.0
            currency = "EUR"
            service_from_date = date(2019, 12, 1)
            service_to_date = date(2019, 12, 31)

            item_generator = InvoiceItemGenerator()
            items = [
                item_generator.generate_title("Hours"),
                item_generator.generate_description("Listing of all hours"),
                item_generator.generate_item("Service", quantity=2, unit="hours", unit_price=65, net_total=130)
            ]

            inv_create = self.moco.Invoice.create(
                project.customer.id,
                recipient_address, 
                creation_date, 
                due_date, 
                service_from_date, 
                service_to_date, 
                title, 
                tax, 
                currency, 
                items, 
                project_id=project.id
            )

            assert inv_create.response.status_code == 200

            assert isinstance(inv_create, JsonResponse)

            assert inv_create.data.project_id == project.id


    def test_create_full(self):
        project = self.get_project()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestInvoice.test_create_full"):
            recipient_address = "Mein Kunde\nHauptstrasse 1\n8000 Zürich"
            creation_date = date(2018, 9, 17)
            due_date = date(2018, 10, 16)
            title = "invoice"
            tax = 8.0
            currency = "EUR"
            service_from_date = date(2019, 12, 1)
            service_to_date = date(2019, 12, 31)

            item_generator = InvoiceItemGenerator()
            items = [
                item_generator.generate_title("Hours"),
                item_generator.generate_description("Listing of all hours"),
                item_generator.generate_item("Service", quantity=2, unit="hours", unit_price=65, net_total=130)
            ]

            change_add = InvoiceChangeAddress.CUSTOMER
            salutation = "salut"
            footer = "this is the footer"
            cash_discount_days = 200
            cash_discount = 10.2

            inv_create = self.moco.Invoice.create(
                customer.id, 
                recipient_address, 
                creation_date, 
                due_date, 
                service_from_date, 
                service_to_date, 
                title, 
                tax, 
                currency, 
                items, 
                status=InvoiceStatus.SENT, 
                change_address=InvoiceChangeAddress.CUSTOMER, 
                salutation=salutation, 
                footer=footer, 
                cash_discount_days=cash_discount_days, 
                cash_discount=cash_discount, 
                project_id=project.id
            )
                    
            assert inv_create.response.status_code == 200
            
            assert isinstance(inv_create, JsonResponse)

            assert inv_create.data.title == "invoice"
            assert inv_create.data.currency == "EUR"
            assert inv_create.data.customer_id == customer.id
            assert inv_create.data.service_period_from == service_from_date.isoformat()
            assert inv_create.data.service_period_to == service_to_date.isoformat()
            assert inv_create.data.date == creation_date.isoformat()
            assert inv_create.data.due_date == due_date.isoformat()
            assert inv_create.data.recipient_address == recipient_address
            assert inv_create.data.tax == tax
            assert inv_create.data.project_id == project.id    
            assert inv_create.data.footer == footer
            assert inv_create.data.cash_discount == cash_discount
            assert inv_create.data.cash_discount_days == cash_discount_days
            
