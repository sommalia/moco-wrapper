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

            response = self.moco.User.create(firstname, lastname, email, password, unit_id)

            assert isinstance(response, JsonResponse)
            assert response.data.firstname == firstname
            assert response.data.lastname == lastname
            assert response.data.email == email
            assert response.data.unit.id == unit_id

            data = response.data

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

            response = self.moco.User.create(firstname, lastname, email, password, unit_id, language=UserLanguage.FR)

            assert isinstance(response, JsonResponse)
            assert response.data.firstname == firstname
            assert response.data.lastname == lastname
            assert response.data.email == email
            assert response.data.unit.id == unit_id

    def test_update(self):
        created_user = self.test_create()

        with self.recorder.use_cassette("TestUser.test_update"):
            new_firstname = "new_firstname"
            response = self.moco.User.update(created_user.id, new_firstname)
            assert isinstance(response, JsonResponse)
            assert response.data.firstname == new_firstname

    def test_delete(self):
        with self.recorder.use_cassette("TestUser.test_delete"):
            unit = self.moco.Unit.getlist()
            unit_id = unit.items[0].id

            firstname = "user to delete"
            lastname = "user to delete"
            email = "email+user+to+delete@email.de"
            password = "password"

            response_create = self.moco.User.create(firstname, lastname, email, password, unit_id)
            user_id_to_delete = response_create.data.id

            response_delete = self.moco.User.delete(user_id_to_delete)
            assert isinstance(response_delete, EmptyResponse)

    def test_get(self):
        created_user = self.test_create()

        with self.recorder.use_cassette("TestUser.test_get"):
            response = self.moco.User.get(created_user.id)
            assert isinstance(response, JsonResponse)
            assert response.data.id == created_user.id
        
    def test_getlist(self):
        with self.recorder.use_cassette("TestUser.test_getlist"):
            response = self.moco.User.getlist()
            assert isinstance(response, ListingResponse)

