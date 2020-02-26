import pytest
from .. import UnitTest

class TestContact(UnitTest):

    def test_create(self):

        firstname = "Peter"
        lastname = "Muster"
        gender = "F"
        organization_id = 123
        title  ="Dr. med."
        job_position = "Account Manager"
        mobile_phone = "+49 177 123 45 67"
        work_fax  = "+49 30 123 45 67"
        work_phone = "+49 30 123 45 67"
        work_email = "bestellung@lieferant.de"
        work_address = "Lieferant AG\nBeispielstrasse 123\n12345 Berlin"
        home_email = "privat@home.ch"
        home_address = "Peter Muster\nZu Hause"
        birthday = "1959-05-22"
        info = "Information for this company"
        tags = ["Christmas Card", "Project Lead"]

        response = self.moco.Contact.create(firstname, lastname, gender, company_id=organization_id, title=title, job_position=job_position, mobile_phone=mobile_phone, work_fax=work_fax, work_phone=work_phone, work_email=work_email, work_address=work_address, home_email=home_email, home_address=home_address, birthday=birthday, info=info, tags=tags)

        data = response["data"]

        assert data["firstname"] == firstname
        assert data["lastname"] == lastname
        assert data["gender"] == gender
        assert data["customer_id"] == organization_id
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
        firstname = "Peter"
        lastname = "Muster"
        gender = "F"
        organization_id = 123
        title  ="Dr. med."
        job_position = "Account Manager"
        mobile_phone = "+49 177 123 45 67"
        work_fax  = "+49 30 123 45 67"
        work_phone = "+49 30 123 45 67"
        work_email = "bestellung@lieferant.de"
        work_address = "Lieferant AG\nBeispielstrasse 123\n12345 Berlin"
        home_email = "privat@home.ch"
        home_address = "Peter Muster\nZu Hause"
        birthday = "1959-05-22"
        info = "Information for this company"
        tags = ["Christmas Card", "Project Lead"]

        response = self.moco.Contact.update(contact_id, firstname=firstname, lastname=lastname, job_position=job_position, gender=gender, company_id=organization_id, title=title, mobile_phone=mobile_phone, work_fax=work_fax, work_phone=work_phone, work_email=work_email, work_address=work_address, home_email=home_email, home_address=home_address, birthday=birthday, info=info, tags=tags)

        data = response["data"]

        assert data["firstname"] == firstname
        assert data["lastname"] == lastname
        assert data["gender"] == gender
        assert data["customer_id"] == organization_id
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

        response = self.moco.Contact.get(contact_id)

        assert response["method"] == "GET"

    def test_getlist(self):
        tags = ["eins", "zwei", "drei", "polizei"]

        response = self.moco.Contact.getlist(tags=tags)
        params = response["params"]

        assert params["tags"] == tags
        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        sort_by = "testfield to sort by"

        response = self.moco.Contact.getlist(sort_by=sort_by)
        
        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "testfield to sort by"
        sort_order = "desc"

        response = self.moco.Contact.getlist(sort_by=sort_by, sort_order=sort_order)
        
        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        page_default = 1

        response = self.moco.Contact.getlist()
        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.Contact.getlist(page=page_overwrite)
        assert response["params"]["page"] == page_overwrite

        
