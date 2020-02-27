from moco_wrapper.util.response import JsonResponse, ListingResponse
from moco_wrapper.models.contact import ContactGender
from moco_wrapper.models.company import CompanyType

from datetime import date

from .. import IntegrationTest

class TestContact(IntegrationTest):
    def get_customer(self):
        with self.recorder.use_cassette("TestContact.get_customer"):
            company_create = self.moco.Company.create(
                "TestContact customer", 
                company_type="customer"
            )

            return company_create.data

    def get_organization(self):
        with self.recorder.use_cassette("TestContact.get_organization"):
            company_create = self.moco.Company.create(
                "TestContact organization",
                company_type="organization"
            )

            return company_create.data

    def get_supplier(self):
        with self.recorder.use_cassette("TestContact.get_supplier"):
            company_create = self.moco.Company.create(
                "TestContact supplier",
                company_type="supplier"
            )

            return company_create.data

    def test_create(self):
        with self.recorder.use_cassette("TestContact.test_create"):
            firstname = "test create"
            lastname = "contact"
            gender = ContactGender.UNDEFINED

            contact_create = self.moco.Contact.create(
                firstname,
                lastname, 
                ContactGender.UNDEFINED
            )
            
            assert contact_create.response.status_code == 200

            assert isinstance(contact_create, JsonResponse)
            
            assert contact_create.data.firstname == firstname
            assert contact_create.data.lastname == lastname
            assert contact_create.data.gender == ContactGender.UNDEFINED

    def test_create_with_organization(self):
        orga = self.get_organization()

        with self.recorder.use_cassette("TestContact.test_create_with_organization"):
            contact_create = self.moco.Contact.create(
                "dummy contact",
                "test create with orga",
                ContactGender.FEMALE,
                company_id=orga.id
            )

            assert contact_create.response.status_code == 200

            assert isinstance(contact_create, JsonResponse)

            assert contact_create.data.company.type == "organization"
            assert contact_create.data.company.id == orga.id
    
    def test_create_with_supplier(self):
        supplier = self.get_supplier()

        with self.recorder.use_cassette("TestContact.test_create_with_supplier"):
            contact_create = self.moco.Contact.create(
                "dummy contact",
                "test create with supplier",
                ContactGender.FEMALE,
                company_id=supplier.id
            )

            assert contact_create.response.status_code == 200

            assert isinstance(contact_create, JsonResponse)

            assert contact_create.data.company.type == "supplier"
            assert contact_create.data.company.id == supplier.id

    def test_create_full(self):
        customer = self.get_customer()

        with self.recorder.use_cassette("TestContact.test_create_full"):
            gender = ContactGender.MALE
            firstname = "peter"
            lastname = "smith"
            title = "dr. med."
            job_position = "intern"
            mobile_phone = "45678"
            
            work_fax = "67890"
            work_phone = "12345"
            work_email = "peter.smith@mycompany.com"
            work_address = "Behind the dumpster at the grocery store"

            home_email = "peter.smith+personal@mycompany.com"
            home_address = "Also behind the dumpster"
            birthday = date(1990, 1, 1)
            info = "Nothing, do not ask"
            tags = ["Homeless", "Dangerous"]

            contact_create = self.moco.Contact.create(
                firstname,
                lastname,
                gender,
                company_id=customer.id,
                title=title,
                job_position=job_position,
                mobile_phone=mobile_phone,
                work_fax=work_fax,
                work_phone=work_phone,
                work_email=work_email,
                work_address=work_address,
                home_address=home_address,
                home_email=home_email,
                birthday=birthday,
                info=info,
                tags=tags
            )

            assert contact_create.response.status_code == 200

            assert isinstance(contact_create, JsonResponse)

            assert contact_create.data.firstname == firstname
            assert contact_create.data.lastname == lastname
            assert contact_create.data.gender == gender
            assert contact_create.data.company.type == "customer"
            assert contact_create.data.company.id == customer.id
            assert contact_create.data.title == title
            assert contact_create.data.job_position == job_position
            assert contact_create.data.mobile_phone == mobile_phone
            assert contact_create.data.work_fax == work_fax
            assert contact_create.data.work_phone == work_phone
            assert contact_create.data.work_email == work_email
            assert contact_create.data.work_address == work_address
            assert contact_create.data.home_address == home_address
            assert contact_create.data.home_email == home_email
            assert contact_create.data.birthday == birthday.isoformat()
            assert contact_create.data.info == info
            assert sorted(contact_create.data.tags) == sorted(tags)

    def test_update(self):
        customer = self.get_customer()

        with self.recorder.use_cassette("TestContact.test_update"):

            contact_create = self.moco.Contact.create(
                "dummy contact",
                "test update",
                ContactGender.UNDEFINED
            )

            gender = ContactGender.MALE
            firstname = "peter"
            lastname = "smith"
            title = "dr. med."
            job_position = "intern"
            mobile_phone = "45678"
            
            work_fax = "67890"
            work_phone = "12345"
            work_email = "peter.smith@mycompany.com"
            work_address = "Behind the dumpster at the grocery store"

            home_email = "peter.smith+personal@mycompany.com"
            home_address = "Also behind the dumpster"
            birthday = date(1990, 1, 1)
            info = "Nothing, do not ask"
            tags = ["Homeless", "Dangerous"]

            contact_update = self.moco.Contact.update(
                contact_create.data.id,
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                company_id=customer.id,
                title=title,
                job_position=job_position,
                mobile_phone=mobile_phone,
                work_fax=work_fax,
                work_phone=work_phone,
                work_email=work_email,
                work_address=work_address,
                home_address=home_address,
                home_email=home_email,
                birthday=birthday,
                info=info,
                tags=tags
            )

            assert contact_create.response.status_code == 200
            assert contact_update.response.status_code == 200

            assert isinstance(contact_create, JsonResponse)
            assert isinstance(contact_update, JsonResponse)

            assert contact_update.data.firstname == firstname
            assert contact_update.data.lastname == lastname
            assert contact_update.data.gender == gender
            assert contact_update.data.company.type == "customer"
            assert contact_update.data.company.id == customer.id
            assert contact_update.data.title == title
            assert contact_update.data.job_position == job_position
            assert contact_update.data.mobile_phone == mobile_phone
            assert contact_update.data.work_fax == work_fax
            assert contact_update.data.work_phone == work_phone
            assert contact_update.data.work_email == work_email
            assert contact_update.data.work_address == work_address
            assert contact_update.data.home_address == home_address
            assert contact_update.data.home_email == home_email
            assert contact_update.data.birthday == birthday.isoformat()
            assert contact_update.data.info == info
            assert sorted(contact_update.data.tags) == sorted(tags)

    def test_get(self):
        with self.recorder.use_cassette("TestContact.test_get"):
            firstname = "test contact"
            lastname = "to get"
            gender = ContactGender.UNDEFINED
            
            contact_create = self.moco.Contact.create(
                firstname, 
                lastname, 
                gender,
            )
            contact_get = self.moco.Contact.get(contact_create.data.id)

            assert contact_create.response.status_code == 200
            assert contact_get.response.status_code == 200

            assert isinstance(contact_get, JsonResponse)

            assert contact_get.data.firstname == firstname
            assert contact_get.data.lastname == lastname
            assert contact_get.data.gender == gender

    def test_getlist(self):
        with self.recorder.use_cassette("TestContact.test_getlist"):
            contact_getlist = self.moco.Contact.getlist()

            assert contact_getlist.response.status_code == 200

            assert isinstance(contact_getlist, ListingResponse)