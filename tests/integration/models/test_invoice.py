from .. import IntegrationTest

from datetime import date

from moco_wrapper.util.response import JsonResponse, ListingResponse, EmptyResponse, FileResponse, ErrorResponse
from moco_wrapper.models.invoice import InvoiceStatus, InvoiceChangeAddress
from moco_wrapper.models.company import CompanyType

from moco_wrapper.util.generator import InvoiceItemGenerator

class TestInvoice(IntegrationTest):
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
        with self.recorder.use_cassette("TestInvoice.test_get"):
            customer_id = self.moco.Company.getlist(company_type=CompanyType.CUSTOMER).items[0].id
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

            inv_create = self.moco.Invoice.create(customer_id, recipient_address, creation_date, due_date, service_from_date, service_to_date, title, tax, currency, items)

            inv_get = self.moco.Invoice.get(inv_create.data.id)


            assert inv_create.response.status_code == 200
            assert inv_get.response.status_code == 200

            assert isinstance(inv_get, JsonResponse)
            assert isinstance(inv_create, JsonResponse)

            assert inv_get.data.customer_id == customer_id
            assert inv_get.data.title == title
            assert inv_get.data.date == creation_date.isoformat()
            assert inv_get.data.recipient_address == recipient_address
            assert inv_get.data.currency == currency
            assert inv_get.data.due_date == due_date.isoformat()

    def test_pdf(self):
        with self.recorder.use_cassette("TestInvoice.test_pdf"):
            customer_id = self.moco.Company.getlist(company_type=CompanyType.CUSTOMER).items[0].id
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

            inv_create = self.moco.Invoice.create(customer_id, recipient_address, creation_date, due_date, service_from_date, service_to_date, title, tax, currency, items)

            inv_pdf = self.moco.Invoice.pdf(inv_create.data.id)

            assert inv_create.response.status_code == 200
            assert inv_pdf.response.status_code == 200

            assert isinstance(inv_create, JsonResponse)
            assert isinstance(inv_pdf, FileResponse)

    def test_timesheet_no_hours(self):
        with self.recorder.use_cassette("TestInvoice.test_timesheet_no_hours"):
            customer_id = self.moco.Company.getlist(company_type=CompanyType.CUSTOMER).items[0].id
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

            inv_create = self.moco.Invoice.create(customer_id, recipient_address, creation_date, due_date, service_from_date, service_to_date, title, tax, currency, items)

            inv_time = self.moco.Invoice.timesheet(inv_create.data.id)
            
            assert inv_create.response.status_code == 200
            assert inv_time.response.status_code == 404

            assert isinstance(inv_create, JsonResponse)
            assert isinstance(inv_time, ErrorResponse)

    def test_update_status(self):
        with self.recorder.use_cassette("TestInvoice.test_update_status"):
            #create minimal invoice
            customer_id = self.moco.Company.getlist(company_type=CompanyType.CUSTOMER).items[0].id
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

            inv_create = self.moco.Invoice.create(customer_id, recipient_address, creation_date, due_date, service_from_date, service_to_date, title, tax, currency, items)
            
            inv_update = self.moco.Invoice.update_status(inv_create.data.id, InvoiceStatus.IGNORED)

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
        with self.recorder.use_cassette("TestInvoice.test_create"):
            customer_id = self.moco.Company.getlist(company_type=CompanyType.CUSTOMER).items[0].id
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

            inv_create = self.moco.Invoice.create(customer_id, recipient_address, creation_date, due_date, service_from_date, service_to_date, title, tax, currency, items)
            
            assert inv_create.response.status_code == 200

            assert isinstance(inv_create, JsonResponse)

            assert inv_create.data.title == "invoice"
            assert inv_create.data.currency == "EUR"
            assert inv_create.data.customer_id == customer_id
            assert inv_create.data.service_period_from == service_from_date.isoformat()
            assert inv_create.data.service_period_to == service_to_date.isoformat()
            assert inv_create.data.date == creation_date.isoformat()
            assert inv_create.data.due_date == due_date.isoformat()
            assert inv_create.data.recipient_address == recipient_address
            assert inv_create.data.tax == tax

    def test_create_with_project(self):
        with self.recorder.use_cassette("TestInvoice.test_create_with_project"):
            customer_id = self.moco.Company.getlist(company_type=CompanyType.CUSTOMER).items[0].id
            
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


            #create a test project (project must belong to the customer)
            user_id = self.moco.User.getlist().items[0].id
            pro_create = self.moco.Project.create("name", "EUR", date(2020, 1, 1), user_id, customer_id)
            project_id = pro_create.data.id

            inv_create = self.moco.Invoice.create(customer_id, recipient_address, creation_date, due_date, service_from_date, service_to_date, title, tax, currency, items, project_id=project_id)


            assert pro_create.response.status_code == 200
            assert inv_create.response.status_code == 200

            assert isinstance(inv_create, JsonResponse)

            assert inv_create.data.project_id == project_id


    def test_create_full(self):
        with self.recorder.use_cassette("TestInvoice.test_create_full"):
            customer_id = self.moco.Company.getlist(company_type=CompanyType.CUSTOMER).items[0].id
            project_id = self.moco.Project.getlist(company_id=customer_id).items[0].id
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

            proj_create_leader_id = self.moco.User.getlist().items[0].id
            proj_create = self.moco.Project.create("invoice test project", "EUR", date(2020, 1, 1), proj_create_leader_id, customer_id)

            inv_create = self.moco.Invoice.create(customer_id, recipient_address, creation_date, due_date, service_from_date, service_to_date, title, tax, currency, items, status=InvoiceStatus.SENT, change_address=InvoiceChangeAddress.CUSTOMER, salutation=salutation, footer=footer, cash_discount_days=cash_discount_days, cash_discount=cash_discount, project_id=proj_create.data.id)
                    
            assert inv_create.response.status_code == 200
            
            assert isinstance(inv_create, JsonResponse)

            assert inv_create.data.title == "invoice"
            assert inv_create.data.currency == "EUR"
            assert inv_create.data.customer_id == customer_id
            assert inv_create.data.service_period_from == service_from_date.isoformat()
            assert inv_create.data.service_period_to == service_to_date.isoformat()
            assert inv_create.data.date == creation_date.isoformat()
            assert inv_create.data.due_date == due_date.isoformat()
            assert inv_create.data.recipient_address == recipient_address
            assert inv_create.data.tax == tax
            assert inv_create.data.project_id == proj_create.data.id    
            assert inv_create.data.footer == footer
            assert inv_create.data.cash_discount == cash_discount
            assert inv_create.data.cash_discount_days == cash_discount_days
            
