import pytest
from .. import UnitTest

from datetime import date

class TestUser(UnitTest):
    def test_create(self):
        firstname = "firstname"
        lastname = "lastname"
        email = "email@email.com"
        password = "this is a very strong password"
        unit_id = 214
        active = True
        external = False
        language = "DE"
        mobile_phone = "2134124 + 123"
        work_phone = "3215 +23 "
        home_address = "this is my home address"
        birthday = date(1994,10,10)
        custom_properties = {
            "custom_shirt": True
        }
        info = "more information"

        response = self.moco.User.create(firstname, lastname, email, password, unit_id, active=active, external=external, language=language, mobile_phone=mobile_phone, work_phone=work_phone, home_address=home_address, birthday=birthday, custom_properties=custom_properties, info=info)
        data = response["data"]

        assert data["firstname"] == firstname
        assert data["lastname"] == lastname
        assert data["email"] == email
        assert data["password"] == password
        assert data["unit_id"] == unit_id
        assert data["active"] == active
        assert data["external"] == external
        assert data["language"] ==  "DE"
        assert data["mobile_phone"] == mobile_phone
        assert data["work_phone"] == work_phone
        assert data["home_address"] == home_address
        assert data["custom_properties"] == custom_properties
        assert data["bday"] == birthday.isoformat()
        assert data["info"] == info

        assert response["method"] == "POST"

    def test_update(self):
        user_id = 1234
        firstname = "firstname"
        lastname = "lastname"
        email = "email@email.com"
        password = "this is a very strong password"
        unit_id = 214
        active = True
        external = False
        language = "DE"
        mobile_phone = "2134124 + 123"
        work_phone = "3215 +23 "
        home_address = "this is my home address"
        birthday = "1994-10-10"
        custom_properties = {
            "custom_shirt": True
        },
        info = "more information"

        response = self.moco.User.update(user_id, firstname=firstname, lastname=lastname, email=email, password=password, unit_id=unit_id, active=active, external=external, language=language, mobile_phone=mobile_phone, work_phone=work_phone, home_address=home_address, birthday=birthday, custom_properties=custom_properties, info=info)
        data = response["data"]

        assert data["firstname"] == firstname
        assert data["lastname"] == lastname
        assert data["email"] == email
        assert data["password"] == password
        assert data["unit_id"] == unit_id
        assert data["active"] == active
        assert data["external"] == external
        assert data["language"] == language
        assert data["mobile_phone"] == mobile_phone
        assert data["work_phone"] == work_phone
        assert data["home_address"] == home_address
        assert data["custom_properties"] == custom_properties
        assert data["bday"] == birthday
        assert data["info"] == info

        assert response["method"] == "PUT"
    
    def test_get(self):
        user_id = 12334

        response = self.moco.User.get(user_id)

        assert response["method"] == "GET"

    def test_getlist(self):
        include_archived = True

        response = self.moco.User.getlist(include_archived=include_archived)

        assert response["params"]["include_archived"] == include_archived
        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        sort_by = "testfield to sort by"

        response = self.moco.User.getlist(sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "testfield to sort by"
        sort_order = "desc"

        response = self.moco.User.getlist(sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        page_default = 1

        response = self.moco.User.getlist()
        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.User.getlist(page=page_overwrite)
        assert response["params"]["page"] == page_overwrite
    
    def test_delete(self):
        user_id = 123

        response = self.moco.User.delete(user_id)

        assert response["method"] == "DELETE"