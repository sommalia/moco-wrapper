import pytest

from moco_wrapper.util.response import JsonResponse, ListingResponse
from moco_wrapper.models.contact import ContactGender
from moco_wrapper.models.company import CompanyType, CompanyCurrency

from datetime import date

from .. import IntegrationTest

class TestContact(IntegrationTest):
    def test_create(self):
        data = {}
        with self.recorder.use_cassette("TestContact.test_create"):
            response = self.moco.Contact.create("first", "last", ContactGender.UNDEFINED)
            data = response.data
            assert isinstance(response, JsonResponse)
            assert response.data != None

        return data

    def test_create_with_company(self):
        with self.recorder.use_cassette("TestContact.test_create_with_company"):
            company_create_response = self.moco.Company.create("test contact company", CompanyType.CUSTOMER, currency=CompanyCurrency.EUR)
            contact_create_response = self.moco.Contact.create("test company contact", "lastname", ContactGender.FEMALE, customer_id=company_create_response.data.id)

            assert isinstance(contact_create_response, JsonResponse)
            assert contact_create_response.data.company.id == company_create_response.data.id

    def test_create_with_birthday(self):
        with self.recorder.use_cassette("TestContact.test_create_with_birthday"):
            response = self.moco.Contact.create("contact with birthday", "lastname", ContactGender.MALE, birthday=date(2000, 1,1))

            assert isinstance(response, JsonResponse)
            assert response.data.birthday == date(2000, 1,1).isoformat()

    def test_create_with_tags(self):
        with self.recorder.use_cassette("TestContact.test_create_with_tags"):
            tags = ["print", "online"]

            response = self.moco.Contact.create("contact with tags", "lastname", ContactGender.UNDEFINED, tags=tags)
            assert isinstance(response, JsonResponse)
            assert response.data.tags.sort() == tags.sort()

    def test_update(self):
        with self.recorder.use_cassette("TestContact.test_update"):
            created_response = self.moco.Contact.create("firstname", "lastname", ContactGender.UNDEFINED)
            response = self.moco.Contact.update(created_response.data.id, firstname="new firstname")
            assert isinstance(response, JsonResponse)
            assert response.data != None


    def test_get(self):
        with self.recorder.use_cassette("TestContact.test_get"):
            created_response = self.moco.Contact.create("firstname", "lastname", ContactGender.UNDEFINED)
            response = self.moco.Contact.get(created_response.data.id)

            assert isinstance(response, JsonResponse)
            assert response.data != None

    def test_getlist(self):
        with self.recorder.use_cassette("TestContact.test_getlist"):
            response = self.moco.Contact.getlist()
            assert isinstance(response, ListingResponse)
            assert response.data != None