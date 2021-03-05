from .. import IntegrationTest

from moco_wrapper.util.response import ObjectResponse, PagedListResponse, EmptyResponse
from datetime import date


class TestUserPresence(IntegrationTest):
    def get_user(self):
        with self.recorder.use_cassette("TestUserPresence.get_user"):
            user = self.moco.User.getlist()[0]
            return user

    def get_unit(self):
        with self.recorder.use_cassette("TestUserPresence.get_unit"):
            unit = self.moco.Unit.getlist()[0]
            return unit

    def get_other_user(self):
        unit = self.get_unit()

        with self.recorder.use_cassette("TestUserPresence.get_other_user"):
            user_create = self.moco.User.create(
                firstname="-",
                lastname="TestUserPresence.get_other_user",
                email="{}@example.org".format(self.id_generator()),
                password=self.id_generator(),
                unit_id=unit.id
            )

            return user_create.data

    def test_create(self):
        with self.recorder.use_cassette("TestUserPresence.test_create"):
            pre_date = self.create_random_date()
            from_time = "08:30"
            to_time = "10:30"

            pre_create = self.moco.UserPresence.create(
                pres_date=pre_date,
                from_time=from_time,
                to_time=to_time
            )

            assert pre_create.response.status_code == 200

            assert type(pre_create) is ObjectResponse

            assert pre_create.data.date is not None
            assert pre_create.data.from_time == from_time
            assert pre_create.data.to_time == to_time
            assert pre_create.data.user.id is not None

    def test_get(self):
        with self.recorder.use_cassette("TestUserPresence.test_get"):
            pre_date = self.create_random_date()
            from_time = "08:30"
            to_time = "10:30"

            pre_create = self.moco.UserPresence.create(
                pres_date=pre_date,
                from_time=from_time,
                to_time=to_time
            )

            pre_get = self.moco.UserPresence.get(
                pres_id=pre_create.data.id
            )

            assert pre_create.response.status_code == 200
            assert pre_get.response.status_code == 200

            assert type(pre_create) is ObjectResponse
            assert type(pre_get) is ObjectResponse

            assert pre_get.data.date is not None
            assert pre_get.data.from_time == from_time
            assert pre_get.data.to_time == to_time
            assert pre_create.data.user.id is not None

    def test_getlist(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestUserPresence.test_getlist"):
            pre_list = self.moco.UserPresence.getlist(
                from_date=date(2020, 1, 1),
                to_date=date(2021, 1, 1),
                user_id=user.id
            )

            assert pre_list.response.status_code == 200

            assert type(pre_list) is PagedListResponse

            assert pre_list.current_page == 1
            assert pre_list.is_last is not None
            assert pre_list.next_page is not None
            assert pre_list.total is not None
            assert pre_list.page_size is not None

    def test_update(self):
        with self.recorder.use_cassette("TestUserPresence.test_update"):
            pre_create = self.moco.UserPresence.create(
                pres_date=self.create_random_date(),
                from_time="10:30",
                to_time="14:00"
            )

            pre_date = self.create_random_date()
            from_time = "08:00"
            to_time = "09:30"

            pre_update = self.moco.UserPresence.update(
                pres_id=pre_create.data.id,
                pres_date=pre_date,
                from_time=from_time,
                to_time=to_time,
            )

            assert pre_create.response.status_code == 200
            assert pre_update.response.status_code == 200

            assert type(pre_create) is ObjectResponse
            assert type(pre_update) is ObjectResponse

            assert pre_update.data.date is not None
            assert pre_update.data.from_time == from_time
            assert pre_update.data.to_time == to_time
            assert pre_create.data.user.id is not None

    def test_delete(self):
        with self.recorder.use_cassette("TestUserPresence.test_delete"):
            pre_create = self.moco.UserPresence.create(
                pres_date=self.create_random_date(),
                from_time="10:00",
                to_time="11:00"
            )

            pre_delete = self.moco.UserPresence.delete(
                pres_id=pre_create.data.id
            )

            assert pre_create.response.status_code == 200
            assert pre_delete.response.status_code == 204

            assert type(pre_create) is ObjectResponse
            assert type(pre_delete) is EmptyResponse

    def test_touch(self):
        with self.recorder.use_cassette("TestUserPresence.test_touch"):
            pre_touch = self.moco.UserPresence.touch()

            # touch it a second time to discard it
            self.moco.UserPresence.touch()

            assert pre_touch.response.status_code == 200

            assert type(pre_touch) is EmptyResponse

    def test_create_impersonate(self):
        other_user = self.get_other_user()

        with self.recorder.use_cassette("TestUserPresence.test_create_impersonate"):
            self.moco.impersonate(
                user_id=other_user.id
            )

            pre_create = self.moco.UserPresence.create(
                pres_date=self.create_random_date(),
                from_time="10:30",
                to_time="10:45"
            )

            assert pre_create.response.status_code == 200

            assert type(pre_create) is ObjectResponse

            assert pre_create.data.user.id == other_user.id

            self.moco.clear_impersonation()
