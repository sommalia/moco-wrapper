from moco_wrapper.util.response import ObjectResponse, PagedListResponse

from .. import IntegrationTest


class TestUnit(IntegrationTest):
    def get_unit(self):
        with self.recorder.use_cassette("TestUnit.get_unit"):
            unit = self.moco.Unit.getlist().items[0]
            return unit

    def test_getlist(self):
        with self.recorder.use_cassette("TestUnit.test_getlist"):
            unit_getlist = self.moco.Unit.getlist()

            assert unit_getlist.response.status_code == 200

            assert type(unit_getlist) is PagedListResponse

            assert unit_getlist.current_page == 1
            assert unit_getlist.is_last is not None
            assert unit_getlist.next_page is not None
            assert unit_getlist.total is not None
            assert unit_getlist.page_size is not None

    def test_get(self):
        unit = self.get_unit()

        with self.recorder.use_cassette("TestUnit.test_get"):
            unit_get = self.moco.Unit.get(
                unit_id=unit.id
            )

            assert unit_get.response.status_code == 200

            assert type(unit_get) is ObjectResponse

            assert unit_get.data.name is not None
            assert unit_get.data.users is not None

    def test_get_unit_with_users(self):
        unit = self.get_unit()

        with self.recorder.use_cassette("TestUnit.test_get_unit_with_users"):
            # create a random user and assign them to our unit
            user_create = self.moco.User.create(
                firstname="-",
                lastname="TestUnit.test_get_unit_with_users_user_create",
                email="{}@example.org".format(self.id_generator()),
                password=self.id_generator(),
                unit_id=unit.id
            )

            unit_get = self.moco.Unit.get(
                unit_id=unit.id
            )

            assert user_create.response.status_code == 200
            assert unit_get.response.status_code == 200

            assert type(user_create) is ObjectResponse
            assert type(unit_get) is ObjectResponse

            assert user_create.data.id in [x.id for x in unit_get.data.users]
