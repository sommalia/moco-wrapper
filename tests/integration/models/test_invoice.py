from .. import IntegrationTest

from datetime import date

from moco_wrapper.util.response import JsonResponse, ListingResponse
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
        #create minimal invoice
        pass

    def test_pdf(self):
        #create minimal invoice
        pass

    def test_timesheet(self):
        #create minimal invoice
        pass

    def test_update_status(self):
        #create minimal invoice
        pass

    def test_create(self):
        with self.recorder.use_cassette("TestInvoice.test_create"):
            customer_id = self.moco.Company.getlist(company_type=CompanyType.CUSTOMER).items[0].id
            project_id = self.moco.Project.getlist().items[0].id
            recipient_address = "sehr geehrte damen und herren"
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
        customer_id = self.moco.Company.getlist(company_type=CompanyType.CUSTOMER).items[0].id
        project_id = self.moco.Project.getlist(company_id=customer_id).items[0].id
        recipient_address = "sehr geehrte damen und herren"
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

        inv_create = self.moco.Invoice.create(customer_id, recipient_address, creation_date, due_date, service_from_date, service_to_date, title, tax, currency, items, project_id=project_id)

        print(inv_create)

        assert inv_create.response.status_code == 200
        assert inv_create.data.project_id == project_id


    def test_create_full(self):
        customer_id = self.moco.Company.getlist(company_type=CompanyType.CUSTOMER).items[0].id
        project_id = self.moco.Project.getlist(company_id=customer_id).items[0].id
        recipient_address = "sehr geehrte damen und herren"
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

        inv_create = self.moco.Invoice.create(customer_id, recipient_address, creation_date, due_date, service_from_date, service_to_date, title, tax, currency, items, status=InvoiceStatus.IGNORED, change_address=InvoiceChangeAddress.CUSTOMER, salutation=salutation, footer=footer, cash_discount_days=cash_discount_days, cash_discount=cash_discount)
                
        assert inv_create.response.status_code == 200
        assert inv_create.data.title == "invoice"
        assert inv_create.data.currency == "EUR"
        assert inv_create.data.customer_id == customer_id
        assert inv_create.data.service_period_from == service_from_date.isoformat()
        assert inv_create.data.service_period_to == service_to_date.isoformat()
        assert inv_create.data.date == creation_date.isoformat()
        assert inv_create.data.due_date == due_date.isoformat()
        assert inv_create.data.recipient_address == recipient_address
        assert inv_create.data.tax == tax
        assert inv_cerate.data.project_id == project_id
        assert inv_create.data.change_address == change_add
        assert inv_create.data.footer == footer
        assert inv_create.data.cash_discount == cash_discount
        assert inv_create.data.cash_discount_days == cash_discount_days
        
