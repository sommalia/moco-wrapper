from moco_wrapper.util.response import JsonResponse, ListingResponse
from moco_wrapper.models.contact import ContactGender
from moco_wrapper.models.company import CompanyType, CompanyCurrency

from datetime import date

from .. import IntegrationTest

class TestContact(IntegrationTest):
    def test_create(self):
        with self.recorder.use_cassette("TestContact.test_create"):
            contact_create = self.moco.Contact.create("first", "last", ContactGender.UNDEFINED)
            data = contact_create.data

            assert contact_create.response.status_code == 200

            assert isinstance(contact_create, JsonResponse)
            assert contact_create.data != None


    def test_create_with_company(self):
        with self.recorder.use_cassette("TestContact.test_create_with_company"):
            company_create = self.moco.Company.create("test contact company", CompanyType.CUSTOMER, currency=CompanyCurrency.EUR)
            contact_create = self.moco.Contact.create("test company contact", "lastname", ContactGender.FEMALE, customer_id=company_create.data.id)

            assert company_create.response.status_code == 200
            assert contact_create.response.status_code == 200

            assert isinstance(contact_create, JsonResponse)
            
            assert contact_create.data.company.id == company_create.data.id

    def test_create_with_birthday(self):
        with self.recorder.use_cassette("TestContact.test_create_with_birthday"):
            contact_create = self.moco.Contact.create("contact with birthday", "lastname", ContactGender.MALE, birthday=date(2000, 1,1))

            assert contact_create.response.status_code == 200

            assert isinstance(contact_create, JsonResponse)
            assert contact_create.data.birthday == date(2000, 1,1).isoformat()

    def test_create_with_tags(self):
        with self.recorder.use_cassette("TestContact.test_create_with_tags"):
            tags = ["print", "online"]

            contact_create = self.moco.Contact.create("contact with tags", "lastname", ContactGender.UNDEFINED, tags=tags)

            assert contact_create.response.status_code == 200

            assert isinstance(contact_create, JsonResponse)
            assert contact_create.data.tags.sort() == tags.sort()

    def test_update(self):
        with self.recorder.use_cassette("TestContact.test_update"):
            contact_create = self.moco.Contact.create("firstname", "lastname", ContactGender.UNDEFINED)
            contact_update = self.moco.Contact.update(contact_create.data.id, firstname="new firstname")
        
            assert contact_create.response.status_code == 200
            assert contact_update.response.status_code == 200

            assert isinstance(contact_update, JsonResponse)

            assert contact_update.data.firstname == "new firstname"


    def test_get(self):
        with self.recorder.use_cassette("TestContact.test_get"):
            contact_create = self.moco.Contact.create("firstname", "lastname", ContactGender.UNDEFINED)
            contact_get = self.moco.Contact.get(contact_create.data.id)

            assert contact_create.response.status_code == 200
            assert contact_get.response.status_code == 200

            assert isinstance(contact_get, JsonResponse)

            assert contact_get.data.firstname == "firstname"

    def test_getlist(self):
        with self.recorder.use_cassette("TestContact.test_getlist"):
            contact_getlist = self.moco.Contact.getlist()

            assert contact_getlist.response.status_code == 200

            assert isinstance(contact_getlist, ListingResponse)

            assert contact_getlist.data != None