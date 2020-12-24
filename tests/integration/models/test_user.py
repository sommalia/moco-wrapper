from moco_wrapper.util.response import ObjectResponse, ErrorResponse, PagedListResponse, EmptyResponse
from datetime import date
from .. import IntegrationTest


class TestUser(IntegrationTest):

    def get_unit(self):
        with self.recorder.use_cassette("TestUser.get_unit"):
            unit = self.moco.Unit.getlist().items[0]
            return unit

    def test_create(self):
        unit = self.get_unit()

        with self.recorder.use_cassette("TestUser.test_create"):
            firstname = "test"
            lastname = "user"
            email = "{}@mycompany.com".format(self.id_generator())
            password = self.id_generator()

            user_create = self.moco.User.create(
                firstname,
                lastname,
                email,
                password,
                unit.id
            )

            assert user_create.response.status_code == 200

            assert type(user_create) is ObjectResponse

            assert user_create.data.firstname == firstname
            assert user_create.data.lastname == lastname
            assert user_create.data.email is not None
            assert user_create.data.unit.id == unit.id

    def test_create_full(self):
        unit = self.get_unit()

        with self.recorder.use_cassette("TestUser.test_create_full"):
            firstname = "test"
            lastname = "user"
            email = "{}@mycompany.com".format(self.id_generator())
            password = self.id_generator()

            active = False
            external = True
            language = "de"
            mobile_phone = "+49 123"
            work_phone = "#49 456"
            home_address = "gen. dumpster diver area 123"
            birthday = date(2020, 1, 1)
            info = "info for this person"

            user_create = self.moco.User.create(
                firstname,
                lastname,
                email,
                password,
                unit.id,
                active=active,
                external=external,
                language=language,
                mobile_phone=mobile_phone,
                work_phone=work_phone,
                home_address=home_address,
                birthday=birthday,
                info=info
            )

            assert user_create.response.status_code == 200

            assert type(user_create) is ObjectResponse

            assert user_create.data.firstname == firstname
            assert user_create.data.lastname == lastname
            assert user_create.data.email is not None
            assert user_create.data.unit.id == unit.id
            assert user_create.data.active == active
            assert user_create.data.extern == external
            assert user_create.data.mobile_phone == mobile_phone
            assert user_create.data.work_phone == work_phone
            assert user_create.data.home_address == home_address
            assert user_create.data.birthday == birthday.isoformat()
            assert user_create.data.info == info

    def test_get(self):
        unit = self.get_unit()

        with self.recorder.use_cassette("TestUser.test_get"):
            firstname = "test"
            lastname = "user"
            email = "{}@mycompany.com".format(self.id_generator())
            password = self.id_generator()

            active = False
            external = True
            language = "de-CH"
            mobile_phone = "+49 123"
            work_phone = "#49 456"
            home_address = "gen. dumpster diver area 123"
            birthday = date(2020, 1, 1)
            info = "info for this person"

            user_create = self.moco.User.create(
                firstname,
                lastname,
                email,
                password,
                unit.id,
                active=active,
                external=external,
                language=language,
                mobile_phone=mobile_phone,
                work_phone=work_phone,
                home_address=home_address,
                birthday=birthday,
                info=info
            )

            user_get = self.moco.User.get(user_create.data.id)

            assert user_create.response.status_code == 200
            assert user_get.response.status_code == 200

            assert type(user_create) is ObjectResponse
            assert type(user_get) is ObjectResponse

            assert user_get.data.firstname == firstname
            assert user_get.data.lastname == lastname
            assert user_get.data.email is not None
            assert user_get.data.unit.id == unit.id
            assert user_get.data.active == active
            assert user_get.data.extern == external
            assert user_get.data.mobile_phone == mobile_phone
            assert user_get.data.work_phone == work_phone
            assert user_get.data.home_address == home_address
            assert user_get.data.birthday == birthday.isoformat()
            assert user_get.data.info == info

    def test_update(self):
        unit = self.get_unit()

        with self.recorder.use_cassette("TestUser.test_update"):
            firstname = "test"
            lastname = "user"
            email = "{}@mycompany.com".format(self.id_generator())
            password = self.id_generator()

            active = False
            external = True
            language = "en"
            mobile_phone = "+49 123"
            work_phone = "#49 456"
            home_address = "gen. dumpster diver area 123"
            birthday = date(2020, 1, 1)
            info = "info for this person"

            user_create = self.moco.User.create(
                "dummy user",
                "test update",
                "{}@mycompany.com".format(self.id_generator()),
                self.id_generator(),
                unit.id
            )

            user_update = self.moco.User.update(
                user_create.data.id,
                firstname=firstname,
                lastname=lastname,
                email=email,
                password=password,
                unit_id=unit.id,
                active=active,
                external=external,
                language=language,
                mobile_phone=mobile_phone,
                work_phone=work_phone,
                home_address=home_address,
                birthday=birthday,
                info=info
            )

            assert user_create.response.status_code == 200
            assert user_update.response.status_code == 200

            assert type(user_create) is ObjectResponse
            assert type(user_update) is ObjectResponse

            assert user_update.data.firstname == firstname
            assert user_update.data.lastname == lastname
            assert user_update.data.email is not None
            assert user_update.data.unit.id == unit.id
            assert user_update.data.active == active
            assert user_update.data.extern == external
            assert user_update.data.mobile_phone == mobile_phone
            assert user_update.data.work_phone == work_phone
            assert user_update.data.home_address == home_address
            assert user_update.data.birthday == birthday.isoformat()
            assert user_update.data.info == info

    def test_delete(self):
        unit = self.get_unit()

        with self.recorder.use_cassette("TestUser.test_delete"):
            user_create = self.moco.User.create(
                "dummy user",
                "test delete",
                "{}@mycompany.com".format(self.id_generator()),
                self.id_generator(),
                unit.id
            )

            user_delete = self.moco.User.delete(user_create.data.id)

            assert user_create.response.status_code == 200
            assert user_delete.response.status_code == 204

            assert type(user_create) is ObjectResponse
            assert type(user_delete) is EmptyResponse

    def test_getlist(self):
        with self.recorder.use_cassette("TestUser.test_getlist"):
            user_getlist = self.moco.User.getlist()

            assert user_getlist.response.status_code == 200

            assert type(user_getlist) is PagedListResponse

            assert user_getlist.current_page == 1
            assert user_getlist.is_last is not None
            assert user_getlist.next_page is not None
            assert user_getlist.total is not None
            assert user_getlist.page_size is not None
