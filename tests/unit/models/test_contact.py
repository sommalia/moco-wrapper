import pytest
from .. import UnitTest


class TestContact(UnitTest):

    def test_create(self):
        firstname = "John"
        lastname = "Doe"
        gender = "M"
        company_id = 123
        title = "Dr."
        job_position = "Account Manager"
        mobile_phone = "177 123 45 67"
        work_fax = "30 123 45 67"
        work_phone = "30 123 45 67"
        work_email = "order@example.org"
        work_address = "21. Main Street"
        home_email = "private@example.org"
        home_address = "John Doe\nat Home"
        birthday = "1959-05-22"
        info = "Information for this company"
        tags = ["Christmas Card", "Project Lead"]

        response = self.moco.Contact.create(
            firstname=firstname,
            lastname=lastname,
            gender=gender,
            company_id=company_id,
            title=title,
            job_position=job_position,
            mobile_phone=mobile_phone,
            work_fax=work_fax,
            work_phone=work_phone,
            work_email=work_email,
            work_address=work_address,
            home_email=home_email,
            home_address=home_address,
            birthday=birthday,
            info=info,
            tags=tags
        )

        data = response["data"]

        assert data["firstname"] == firstname
        assert data["lastname"] == lastname
        assert data["gender"] == gender
        assert data["company_id"] == company_id
        assert data["title"] == title
        assert data["job_position"] == job_position
        assert data["mobile_phone"] == mobile_phone
        assert data["work_fax"] == work_fax
        assert data["work_phone"] == work_phone
        assert data["work_email"] == work_email
        assert data["work_address"] == work_address
        assert data["home_email"] == home_email
        assert data["home_address"] == home_address
        assert data["birthday"] == birthday
        assert data["info"] == info
        assert data["tags"] == tags

        assert response["method"] == "POST"

    def test_update(self):
        contact_id = 123
        firstname = "John"
        lastname = "Doe"
        gender = "M"
        company_id = 123
        title = "Dr."
        job_position = "Account Manager"
        mobile_phone = "177 123 45 67"
        work_fax = "30 123 45 67"
        work_phone = "30 123 45 67"
        work_email = "order@example.org"
        work_address = "21. Main Street"
        home_email = "private@example.org"
        home_address = "John Doe\nat Home"
        birthday = "1959-05-22"
        info = "Information for this company"
        tags = ["Christmas Card", "Project Lead"]

        response = self.moco.Contact.update(
            contact_id=contact_id,
            firstname=firstname,
            lastname=lastname,
            job_position=job_position,
            gender=gender,
            company_id=company_id,
            title=title,
            mobile_phone=mobile_phone,
            work_fax=work_fax,
            work_phone=work_phone,
            work_email=work_email,
            work_address=work_address,
            home_email=home_email,
            home_address=home_address,
            birthday=birthday,
            info=info,
            tags=tags
        )

        data = response["data"]

        assert data["firstname"] == firstname
        assert data["lastname"] == lastname
        assert data["gender"] == gender
        assert data["company_id"] == company_id
        assert data["title"] == title
        assert data["job_position"] == job_position
        assert data["mobile_phone"] == mobile_phone
        assert data["work_fax"] == work_fax
        assert data["work_phone"] == work_phone
        assert data["work_email"] == work_email
        assert data["work_address"] == work_address
        assert data["home_email"] == home_email
        assert data["home_address"] == home_address
        assert data["birthday"] == birthday
        assert data["info"] == info
        assert data["tags"] == tags

        assert response["method"] == "PUT"

    def test_get(self):
        contact_id = 1234

        response = self.moco.Contact.get(
            contact_id=contact_id
        )

        assert response["method"] == "GET"

    def test_getlist(self):
        tags = ["first", "seconds", "third", "fourth"]

        response = self.moco.Contact.getlist(
            tags=tags
        )

        params = response["params"]

        assert params["tags"] == tags
        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        sort_by = "testfield to sort by"

        response = self.moco.Contact.getlist(
            sort_by=sort_by
        )

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "field to sort by"
        sort_order = "desc"

        response = self.moco.Contact.getlist(
            sort_by=sort_by,
            sort_order=sort_order
        )

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        page_default = 1

        response = self.moco.Contact.getlist()

        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.Contact.getlist(
            page=page_overwrite
        )

        assert response["params"]["page"] == page_overwrite

    def test_getlist_phone(self):
        phone = "test phone number"

        response = self.moco.Contact.getlist(
            phone=phone
        )

        params = response["params"]

        assert params["phone"] == phone
        assert response["method"] == "GET"

    def test_getlist_term(self):
        term = "test term"

        response = self.moco.Contact.getlist(
            term=term
        )

        params = response["params"]

        assert params["term"] == term
        assert response["method"] == "GET"
