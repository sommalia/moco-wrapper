from moco_wrapper.util.response import JsonResponse, ListingResponse
from moco_wrapper.models.company import CompanyType

import string
import random

from .. import IntegrationTest

class TestCompany(IntegrationTest):
    def get_user(self):
        with self.recorder.use_cassette("TestCompany.get_user"):
            user = self.moco.User.getlist().items[0]
            return user


    def test_create_customer(self):
        with self.recorder.use_cassette("TestCompany.test_create_customer"):
            name = "company create customer"
            company_create = self.moco.Company.create(
                name,
                CompanyType.CUSTOMER
            )

            assert company_create.response.status_code == 200

            assert isinstance(company_create, JsonResponse)

            assert company_create.data.name == name
            assert company_create.data.type == CompanyType.CUSTOMER

    def test_create_supplier(self):
        with self.recorder.use_cassette("TestCompany.test_create_supplier"):
            name = "company create supplier"
            company_create = self.moco.Company.create(
                name,
                CompanyType.SUPPLIER
            )

            assert company_create.response.status_code == 200

            assert isinstance(company_create, JsonResponse)

            assert company_create.data.name == name
            assert company_create.data.type == CompanyType.SUPPLIER

    def test_create_orga(self):
        with self.recorder.use_cassette("TestCompany.test_create_orga"):
            name = "company create organization"
            company_create = self.moco.Company.create(
                name,
                CompanyType.ORGANIZATION
            )

            assert company_create.response.status_code == 200

            assert isinstance(company_create, JsonResponse)

            assert company_create.data.name == name
            assert company_create.data.type == CompanyType.ORGANIZATION

    def test_create_full(self):
        user = self.get_user()

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
            currency = "EUR"
            identifier = self.id_generator()
            billing_tax = 25.5
            default_invoice_due_days = 15
            country_code = "CH"
            footer="this is the footer"
            vat="CHE123456789"

            company_create = self.moco.Company.create(
                name,
                company_type,
                website=website,
                fax=fax,
                phone=phone,
                email=email,
                address=address,
                info=info,
                custom_properties=custom_properties,
                labels=labels,
                user_id=user.id,
                currency=currency,
                identifier=identifier,
                billing_tax=billing_tax,
                country_code=country_code,
                footer=footer,
                vat_identifier=vat,
                default_invoice_due_days=default_invoice_due_days
            )

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
            assert company_create.data.user.id == user.id
            assert company_create.data.currency == currency
            assert company_create.data.identifier is not None
            assert company_create.data.billing_tax == billing_tax
            assert company_create.data.default_invoice_due_days == default_invoice_due_days
            assert company_create.data.country_code == country_code
            assert company_create.data.footer == footer
            assert company_create.data.vat_identifier == vat

    def test_update(self):
        with self.recorder.use_cassette("TestCompany.test_update"):
            company_create = self.moco.Company.create(
                "dummy company, test update",
                CompanyType.CUSTOMER
            )

            name = "test company updated name"
            website = "https://myownwebsite.com"
            labels = ["these", "are", "the", "labels"]

            company_update = self.moco.Company.update(
                company_create.data.id,
                name=name,
                website=website,
                labels=labels
            )

            assert company_create.response.status_code == 200
            assert company_update.response.status_code == 200

            assert isinstance(company_update, JsonResponse)

            assert company_update.data.name == name
            assert company_update.data.website == website
            assert sorted(company_update.data.labels) == sorted(labels)

    def test_update_full(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestCompany.test_update_full"):
            company_create = self.moco.Company.create(
                "dummy company, test update full",
                CompanyType.CUSTOMER
            )

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
            currency = "EUR"
            identifier = self.id_generator()
            billing_tax = 25.5
            default_invoice_due_days = 15
            country_code = "CH"
            footer = "this is the updated footer"
            vat = "CHE987654321"

            company_update = self.moco.Company.update(
                company_create.data.id,
                company_type=company_type,
                name=name,
                website=website,
                fax=fax,
                phone=phone,
                email=email,
                address=address,
                info=info,
                custom_properties=custom_properties,
                labels=labels,
                user_id=user.id,
                currency=currency,
                identifier=identifier,
                billing_tax=billing_tax,
                default_invoice_due_days=default_invoice_due_days,
                country_code=country_code,
                footer=footer,
                vat_identifier=vat
            )

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
            assert company_update.data.user.id == user.id
            assert company_update.data.currency == currency
            assert company_update.data.identifier is not None
            assert company_update.data.billing_tax == billing_tax
            assert company_update.data.default_invoice_due_days == default_invoice_due_days
            assert company_update.data.country_code == country_code
            assert company_update.data.footer == footer
            assert company_update.data.vat_identifier == vat

    def test_get(self):
        with self.recorder.use_cassette("TestCompany.test_get"):
            name = "company to get"
            company_create = self.moco.Company.create(
                name,
                CompanyType.CUSTOMER
            )
            company_get = self.moco.Company.get(company_create.data.id)

            assert company_create.response.status_code == 200
            assert company_get.response.status_code == 200

            assert isinstance(company_get, JsonResponse)

            assert company_get.data.name == name
            assert company_get.data.type == CompanyType.CUSTOMER

    def test_getlist(self):
        with self.recorder.use_cassette("TestCompany.test_getlist"):
            company_getlist = self.moco.Company.getlist()

            assert company_getlist.response.status_code == 200

            assert isinstance(company_getlist, ListingResponse)

            assert company_getlist.current_page == 1
            assert company_getlist.is_last is not None
            assert company_getlist.next_page is not None
            assert company_getlist.total is not None
            assert company_getlist.page_size is not None

    def test_create_supplier_with_iban(self):
        with self.recorder.use_cassette("TestCompany.test_create_supplier_with_iban"):
            iban = "FI0342541877156574" # random iban
            company_create = self.moco.Company.create(
                "supplier with iban",
                CompanyType.SUPPLIER,
                iban=iban
            )

            assert company_create.response.status_code == 200


            assert isinstance(company_create, JsonResponse)

            assert company_create.data.iban == iban

    def test_create_customer_with_vat(self):
        with self.recorder.use_cassette("TestCompany.test_create_customer_with_vat"):
            vat = "DE123456789"
            company_create = self.moco.Company.create(
                "customer with vat",
                CompanyType.CUSTOMER,
                vat_identifier=vat
            )

            assert company_create.response.status_code == 200

            assert isinstance(company_create, JsonResponse)

            assert company_create.data.vat_identifier == vat

    def test_update_iban(self):
        with self.recorder.use_cassette("TestCompany.test_update_iban"):
            iban = "FI0342541877156574" # random iban

            company_create = self.moco.Company.create(
                "dummy company, update iban",
                CompanyType.SUPPLIER,
            )

            company_update = self.moco.Company.update(
                company_create.data.id,
                iban=iban
            )

            assert company_create.response.status_code == 200
            assert company_update.response.status_code == 200

            assert isinstance(company_create, JsonResponse)
            assert isinstance(company_update, JsonResponse)

            assert company_update.data.iban == iban

