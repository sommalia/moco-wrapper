import pytest

from .. import UnitTest

class TestCompany(UnitTest):

    def test_create(self):
        name = "test company"
        company_type = "customer"
        website = "https://example.com"
        fax = "1234"
        phone = "12345"
        email = "example@example.org"
        address = "here is the address 25 street"
        info = "more information about the company"
        custom_properties = {
            "test": "test"
        }

        labels = ["best", "company", "ever"]
        user_id = 12
        currency = "EUR"
        identifier = "COMP-1"
        billing_tax = 21
        default_invoice_due_days = 22

        response = self.moco.Company.create(name, company_type, website=website, fax=fax, phone=phone, email=email, address=address, info=info, custom_properties=custom_properties, labels=labels, user_id=user_id, currency=currency, identifier=identifier, billing_tax=billing_tax, default_invoice_due_days=default_invoice_due_days)

        data = response["data"]

        assert data["name"] == name
        assert data["type"] == company_type
        assert data["website"] == website
        assert data["fax"] == fax
        assert data["phone"] == phone
        assert data["email"] == email
        assert data["address"] == address
        assert data["info"] == info
        assert data["custom_properties"] == custom_properties
        assert data["labels"] == labels
        assert data["user_id"] == user_id
        assert data["currency"] == currency
        assert data["identifier"] == identifier
        assert data["billing_tax"] == billing_tax
        assert data["invoice_due_days"] == default_invoice_due_days

        assert response["method"] == "POST"#
    
    def test_update(self):
        company_id = 1234
        company_type = "customer"
        name = "test company"
        website = "https://example.com"
        fax = "1234"
        phone = "12345"
        email = "example@example.org"
        address = "here is the address 25 street"
        info = "more information about the company"
        custom_properties = {
            "test": "test"
        }

        labels = ["best", "company", "ever"]
        user_id = 12
        currency = "EUR"
        identifier = "COMP-1"
        billing_tax = 21
        default_invoice_due_days = 22

        response = self.moco.Company.update(company_id, company_type=company_type, name=name, website=website, fax=fax, phone=phone, email=email, address=address, info=info, custom_properties=custom_properties, labels=labels, user_id=user_id, currency=currency, identifier=identifier, billing_tax=billing_tax, default_invoice_due_days=default_invoice_due_days)

        data = response["data"]

        assert data["name"] == name
        assert data["type"] == company_type
        assert data["website"] == website
        assert data["fax"] == fax
        assert data["phone"] == phone
        assert data["email"] == email
        assert data["address"] == address
        assert data["info"] == info
        assert data["custom_properties"] == custom_properties
        assert data["labels"] == labels
        assert data["user_id"] == user_id
        assert data["currency"] == currency
        assert data["identifier"] == identifier
        assert data["billing_tax"] == billing_tax
        assert data["invoice_due_days"] == default_invoice_due_days

        assert response["method"] == "PUT"

    def test_get(self):
        company_id = 1234

        response = self.moco.Company.get(company_id)

        assert response["method"] == "GET"

    def test_getlist(self):
        company_type = "supplier",
        tags = ["test", "this", "list"],
        identifier = "COMP-3",

        response = self.moco.Company.getlist(company_type=company_type, tags=tags, identifier=identifier)
        params = response["params"]

        assert params["tags"] == tags
        assert params["type"] == company_type
        assert params["identifier"] == identifier

        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        sort_by = "test sort field"

        response = self.moco.Company.getlist(sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by) 

    def test_getlist_sort_overwrite(self):
        sort_by = "test sort field"
        sort_order = "desc"

        response = self.moco.Company.getlist(sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order) 

    def test_getlist_page_default(self):
        page_default = 1

        response = self.moco.Company.getlist()
        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.Company.getlist(page=page_overwrite)
        assert response["params"]["page"] == page_overwrite

    def test_create_supplier_with_iban(self):
        iban = "CH1234"

        response = self.moco.Company.create("test company", company_type="supplier", iban=iban)

        assert response["data"]["iban"] == iban


    def test_create_supplier_with_vat(self):
        vat = "12345"

        response = self.moco.Company.create("test company", company_type="supplier", vat_identifier=vat)

        assert response["data"]["vat_identifier"] == vat

    def test_create_customer_with_vat(self):
        vat = "12345"

        response = self.moco.Company.create("test company", company_type="supplier", vat_identifier=vat)

        assert response["data"]["vat_identifier"] == vat

    def test_create_vat_omitted_in_orga(self):
        vat = "12345"

        response = self.moco.Company.create("test company", company_type="organization", vat_identifier=vat)

        assert "vat_identifier" not in response["data"].keys()

    def test_create_iban_omitted_in_customer(self):
        iban = "CHF1234"

        response = self.moco.Company.create("test company", company_type="customer", iban=iban)

        assert "iban" not in response["data"].keys()

    
    def test_create_iban_omitted_in_orga(self):
        iban = "CHF1234"

        response = self.moco.Company.create("test company", company_type="organization", iban=iban)

        assert "vat_identifier" not in response["data"].keys()

    def test_update_iban(self):
        iban = "CHF1234"

        response = self.moco.Company.update(1, iban=iban)

        assert response["data"]["iban"] == iban

    def test_update_vat(self):
        vat = "12345"

        response = self.moco.Company.update(1, vat_identifier=vat)

        assert response["data"]["vat_identifier"] == vat 
        