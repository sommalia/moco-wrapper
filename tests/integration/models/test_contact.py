from moco_wrapper.util.response import ObjectResponse, PagedListResponse
from moco_wrapper.models.contact import ContactGender
from moco_wrapper.models.company import CompanyType

from datetime import date

from .. import IntegrationTest


class TestContact(IntegrationTest):
    def get_customer(self):
        with self.recorder.use_cassette("TestContact.get_customer"):
            company_create = self.moco.Company.create(
                name="TestContact.get_customer",
                company_type=CompanyType.CUSTOMER
            )

            return company_create.data

    def get_organization(self):
        with self.recorder.use_cassette("TestContact.get_organization"):
            company_create = self.moco.Company.create(
                name="TestContact.get_organization",
                company_type=CompanyType.ORGANIZATION
            )

            return company_create.data

    def get_supplier(self):
        with self.recorder.use_cassette("TestContact.get_supplier"):
            company_create = self.moco.Company.create(
                name="TestContact.get_supplier",
                company_type=CompanyType.SUPPLIER
            )

            return company_create.data

    def test_create(self):
        with self.recorder.use_cassette("TestContact.test_create"):
            firstname = "-"
            lastname = "TestContact.test_create"
            gender = ContactGender.UNDEFINED

            contact_create = self.moco.Contact.create(
                firstname=firstname,
                lastname=lastname,
                gender=gender
            )

            assert contact_create.response.status_code == 200

            assert type(contact_create) is ObjectResponse

            assert contact_create.data.firstname == firstname
            assert contact_create.data.lastname == lastname
            assert contact_create.data.gender == ContactGender.UNDEFINED

    def test_create_with_organization(self):
        organization = self.get_organization()

        with self.recorder.use_cassette("TestContact.test_create_with_organization"):
            contact_create = self.moco.Contact.create(
                firstname="-",
                lastname="TestContact.test_create_with_organization",
                gender=ContactGender.FEMALE,
                company_id=organization.id
            )

            assert contact_create.response.status_code == 200

            assert type(contact_create) is ObjectResponse

            assert contact_create.data.company.type == "organization"
            assert contact_create.data.company.id == organization.id

    def test_create_with_supplier(self):
        supplier = self.get_supplier()

        with self.recorder.use_cassette("TestContact.test_create_with_supplier"):
            contact_create = self.moco.Contact.create(
                firstname="-",
                lastname="TestContact.test_create_with_supplier",
                gender=ContactGender.FEMALE,
                company_id=supplier.id
            )

            assert contact_create.response.status_code == 200

            assert type(contact_create) is ObjectResponse

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
            work_email = "peter.smith@example.org"
            work_address = "21. Main Street"

            home_email = "peter.smith+personal@example.org"
            home_address = "22. Second Street"
            birthday = date(1990, 1, 1)
            info = "He is an important test contact"
            tags = ["Important", "Test"]

            contact_create = self.moco.Contact.create(
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

            assert type(contact_create) is ObjectResponse

            assert contact_create.data.firstname == firstname
            assert contact_create.data.lastname == lastname
            assert contact_create.data.gender == gender
            assert contact_create.data.company.type == CompanyType.CUSTOMER
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
                firstname="-",
                lastname="TestContact.test_update_creat",
                gender=ContactGender.UNDEFINED
            )

            gender = ContactGender.MALE
            firstname = "peter"
            lastname = "smith"
            title = "dr. med."
            job_position = "intern"
            mobile_phone = "45678"

            work_fax = "67890"
            work_phone = "12345"
            work_email = "peter.smith@example.org"
            work_address = "21. Main Street"

            home_email = "peter.smith+personal@example.org"
            home_address = "22. Main Street"
            birthday = date(1990, 1, 1)
            info = "He is an important test contact"
            tags = ["Important", "Test"]

            contact_update = self.moco.Contact.update(
                contact_id=contact_create.data.id,
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

            assert type(contact_create) is ObjectResponse
            assert type(contact_update) is ObjectResponse

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
            firstname = "-"
            lastname = "TestContact.test_get_create"
            gender = ContactGender.UNDEFINED

            contact_create = self.moco.Contact.create(
                firstname=firstname,
                lastname=lastname,
                gender=gender,
            )
            contact_get = self.moco.Contact.get(
                contact_id=contact_create.data.id
            )

            assert contact_create.response.status_code == 200
            assert contact_get.response.status_code == 200

            assert type(contact_get) is ObjectResponse

            assert contact_get.data.firstname == firstname
            assert contact_get.data.lastname == lastname
            assert contact_get.data.gender == gender

    def test_getlist(self):
        with self.recorder.use_cassette("TestContact.test_getlist"):
            contact_getlist = self.moco.Contact.getlist()

            assert contact_getlist.response.status_code == 200

            assert type(contact_getlist) is PagedListResponse

            assert contact_getlist.current_page == 1
            assert contact_getlist.is_last is not None
            assert contact_getlist.next_page is not None
            assert contact_getlist.total is not None
            assert contact_getlist.page_size is not None

    def test_getlist_phone(self):
        with self.recorder.use_cassette("TestContact.test_getlist_phone"):
            phone = '+49 123 12345'
            contact_create = self.moco.Contact.create(
                firstname="-",
                lastname="TestContact.test_getlist_phone_create",
                gender=ContactGender.MALE,
                work_phone=phone)

            contact_getlist = self.moco.Contact.getlist(
                phone=phone
            )

            assert contact_create.response.status_code == 200
            assert contact_getlist.response.status_code == 200

            assert type(contact_create) is ObjectResponse
            assert type(contact_getlist) is PagedListResponse

            assert contact_create.data.id in [x.id for x in contact_getlist.items]

    def test_getlist_term(self):
        with self.recorder.use_cassette("TestContact.test_getlist_term"):
            term = "dummy contact to search by term"

            contact_create = self.moco.Contact.create(
                firstname=term,
                lastname="TestContact.test_getlist_term",
                gender=ContactGender.FEMALE
            )

            contact_getlist = self.moco.Contact.getlist(
                term=term
            )

            assert contact_create.response.status_code == 200
            assert contact_getlist.response.status_code == 200

            assert type(contact_create) is ObjectResponse
            assert type(contact_getlist) is PagedListResponse

            assert contact_create.data.id in [x.id for x in contact_getlist.items]
