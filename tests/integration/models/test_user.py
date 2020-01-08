import pytest

from moco_wrapper.util.response import JsonResponse, ErrorResponse, ListingResponse, EmptyResponse
from moco_wrapper.models.user import UserLanguage

from .. import IntegrationTest

class TestUser(IntegrationTest):

    def test_create(self):
        data = {}

        with self.recorder.use_cassette("TestUser.test_create"):
            unit = self.moco.Unit.getlist()
            unit_id = unit.items[0].id

            firstname = "testfirstname"
            lastname = "testlastname"
            email = "email@email.de"
            password = "password"

            user_create = self.moco.User.create(firstname, lastname, email, password, unit_id)

            assert user_create.response.status_code == 200

            assert isinstance(user_create, JsonResponse)

            assert user_create.data.firstname == firstname
            assert user_create.data.lastname == lastname
            assert user_create.data.email == email
            assert user_create.data.unit.id == unit_id
           
            data = user_create.data

        return data

    def test_create_with_language(self):
        with self.recorder.use_cassette("TestUser.test_create_with_language"):
            unit = self.moco.Unit.getlist()
            unit_id = unit.items[0].id

            firstname = "user with other language"
            lastname = "testlastname"
            email = "email+user+with+language@email.de"
            password = "password"
            language = UserLanguage.FR

            user_create = self.moco.User.create(firstname, lastname, email, password, unit_id, language=UserLanguage.FR)

            assert user_create.response.status_code == 200  

            assert isinstance(user_create, JsonResponse)

            assert user_create.data.firstname == firstname
            assert user_create.data.lastname == lastname
            assert user_create.data.email == email
            assert user_create.data.unit.id == unit_id

    def test_update(self):
        created_user = self.test_create()

        with self.recorder.use_cassette("TestUser.test_update"):
            new_firstname = "new_firstname"
            user_update = self.moco.User.update(created_user.id, new_firstname)

            assert user_update.response.status_code == 200

            assert isinstance(user_update, JsonResponse)

            assert user_update.data.firstname == new_firstname

    def test_delete(self):
        with self.recorder.use_cassette("TestUser.test_delete"):
            unit = self.moco.Unit.getlist()
            unit_id = unit.items[0].id

            firstname = "user to delete"
            lastname = "user to delete"
            email = "email+user+to+delete@email.de"
            password = "password"

            user_create = self.moco.User.create(firstname, lastname, email, password, unit_id)
            user_delete = self.moco.User.delete(user_create.data.id)

            assert user_create.response.status_code == 200
            assert user_delete.response.status_code == 204

            assert isinstance(user_delete, EmptyResponse)

    def test_get(self):
        created_user = self.test_create()

        with self.recorder.use_cassette("TestUser.test_get"):
            user_get = self.moco.User.get(created_user.id)

            assert user_get.response.status_code == 200
            
            assert isinstance(user_get, JsonResponse)

            assert user_get.data.id == created_user.id
        
    def test_getlist(self):
        with self.recorder.use_cassette("TestUser.test_getlist"):
            user_getlist = self.moco.User.getlist()

            assert user_getlist.response.status_code == 200

            assert isinstance(user_getlist, ListingResponse)

