from moco_wrapper.util.response import JsonResponse, ListingResponse
from moco_wrapper.models.company import CompanyCurrency, CompanyType

from .. import IntegrationTest

class TestCompany(IntegrationTest):
    def test_create_customer(self):
        with self.recorder.use_cassette("TestCompany.test_create_customer"):
            company_create = self.moco.Company.create("test company customer", CompanyType.CUSTOMER)

            assert company_create.response.status_code == 200

            assert isinstance(company_create, JsonResponse)

            assert company_create.data.name == "test company customer"
            assert company_create.data.type == "customer"

    def test_create_supplier(self):
        with self.recorder.use_cassette("TestCompany.test_create_supplier"):
            company_create = self.moco.Company.create("test company supplier", CompanyType.SUPPLIER)

            assert company_create.response.status_code == 200

            assert isinstance(company_create, JsonResponse)

            assert company_create.data.name == "test company supplier"
            assert company_create.data.type == "supplier"

    def test_create_orga(self):
        with self.recorder.use_cassette("TestCompany.test_create_orga"):
            company_create = self.moco.Company.create("test company orga", CompanyType.ORGANIZATION)

            assert company_create.response.status_code == 200

            assert isinstance(company_create, JsonResponse)

            assert company_create.data.name == "test company orga"
            assert company_create.data.type == "organization"

    def test_create_full(self):
        with self.recorder.use_cassette("TestCompany.test_create_full"):    
            name = "company every prop set"
            company_type = "customer"
            website = "https://mocoapp.com"
            fax = "12345"
            phone = "12345"
            email = "test@test.de"
            address = "test street 1"
            info = "in this company every property is set"
            custom_properties = {"test": "test"}
            labels = ["these", "are", "labels"]
            user_id = self.moco.User.getlist().items[0].id
            currency = "EUR"
            identifier = "COMP-T-9"
            billing_tax = 25.5
            default_invoice_due_days = 15
            country_code = "CH"

            company_create = self.moco.Company.create(name, company_type, website=website, fax=fax, phone=phone, email=email, address=address, info=info, custom_properties=custom_properties, labels=labels, user_id=user_id, currency=currency, identifier=identifier, billing_tax=billing_tax, default_invoice_due_days=default_invoice_due_days , country_code=country_code)

            assert company_create.response.status_code == 200

            assert isinstance(company_create, JsonResponse)

            assert company_create.data.name == name
            assert company_create.data.type == company_type
            assert company_create.data.website == website
            assert company_create.data.fax == fax
            assert company_create.data.phone == phone
            assert company_create.data.email == email
            assert company_create.data.address == address
            assert company_create.data.info == info
            assert sorted(company_create.data.labels) == sorted(labels)
            assert company_create.data.user.id == user_id
            assert company_create.data.currency == currency
            assert company_create.data.identifier == identifier
            assert company_create.data.billing_tax == billing_tax
            assert company_create.data.default_invoice_due_days == default_invoice_due_days
            assert company_create.data.country_code == country_code

    def test_update(self):
        with self.recorder.use_cassette("TestCompany.test_update"):
            company_create = self.moco.Company.create("test company to update", CompanyType.CUSTOMER)
            company_update = self.moco.Company.update(company_create.data.id, name="updated company name", website="https://mocoapp.com", labels=["these", "are", "labels"])

            assert company_create.response.status_code == 200
            assert company_update.response.status_code == 200

            assert isinstance(company_update, JsonResponse)

            assert company_update.data.website == "https://mocoapp.com"
            assert company_update.data.name == "updated company name"

    def test_update_full(self):
        with self.recorder.use_cassette("TestCompany.test_update_full"):
            company_create = self.moco.Company.create("test company to update", CompanyType.CUSTOMER)

            name = "updated company with  prop set"
            company_type = "customer"
            website = "https://mocoapp.com"
            fax = "12345"
            phone = "12345"
            email = "test@test.de"
            address = "test street 1"
            info = "in this company every property is set"
            custom_properties = {"test": "test"}
            labels = ["these", "are", "labels"]
            user_id = self.moco.User.getlist().items[0].id
            currency = "EUR"
            identifier = "COMP-U-7"
            billing_tax = 25.5
            default_invoice_due_days = 15
            country_code = "CH"

            company_update = self.moco.Company.update(company_create.data.id, company_type=company_type, name=name, website=website, fax=fax, phone=phone, email=email, address=address, info=info, custom_properties=custom_properties, labels=labels, user_id=user_id, currency=currency, identifier=identifier, billing_tax=billing_tax, default_invoice_due_days=default_invoice_due_days, country_code=country_code)

            print(company_update)

            assert company_create.response.status_code == 200
            assert company_update.response.status_code == 200

            assert isinstance(company_update, JsonResponse)

            assert company_update.data.name == name
            assert company_update.data.type == company_type
            assert company_update.data.website == website
            assert company_update.data.fax == fax
            assert company_update.data.phone == phone
            assert company_update.data.email == email
            assert company_update.data.address == address
            assert company_update.data.info == info
            assert sorted(company_update.data.labels) == sorted(labels)
            assert company_update.data.user.id == user_id
            assert company_update.data.currency == currency
            assert company_update.data.identifier == identifier
            assert company_update.data.billing_tax == billing_tax
            assert company_update.data.default_invoice_due_days == default_invoice_due_days
            assert company_update.data.country_code == country_code

    def test_get(self):
        with self.recorder.use_cassette("TestCompany.test_get"):
            company_create = self.moco.Company.create("test company get", CompanyType.CUSTOMER)
            company_get = self.moco.Company.get(company_create.data.id)

            assert company_create.response.status_code == 200
            assert company_get.response.status_code == 200

            assert isinstance(company_get, JsonResponse)

            assert company_get.data.name == "test company get"
            assert company_get.data.type == "customer"

    def test_getlist(self):
        with self.recorder.use_cassette("TestCompany.test_getlist"):
            company_getlist = self.moco.Company.getlist()

            assert company_getlist.response.status_code == 200

            assert isinstance(company_getlist, ListingResponse)
