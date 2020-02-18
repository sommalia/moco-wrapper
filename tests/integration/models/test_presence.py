from .. import IntegrationTest

from moco_wrapper.util.response import JsonResponse, ListingResponse, EmptyResponse
from datetime import date

class TestPresence(IntegrationTest):
    def get_user(self):
        with self.recorder.use_cassette("TestPresence.get_user"):
            user = self.moco.User.getlist().items[0]
            return user

    def test_create(self):
        with self.recorder.use_cassette("TestPresence.test_create"):
            pre_date = date(2020, 1, 20)
            from_time  = "08:30"
            to_time = "10:30"

            pre_create = self.moco.Presence.create(pre_date, from_time, to_time)

            assert pre_create.response.status_code == 200
            
            assert isinstance(pre_create, JsonResponse)
            
            assert pre_create.data.date == pre_date.isoformat()
            assert pre_create.data.from_time == from_time
            assert pre_create.data.to_time == to_time

    def test_get(self):
        with self.recorder.use_cassette("TestPresence.test_get"):
            pre_date = date(2020, 2, 1)
            from_time  = "08:30"
            to_time = "10:30"

            pre_create = self.moco.Presence.create(pre_date, from_time, to_time)
            pre_get = self.moco.Presence.get(pre_create.data.id)

            assert pre_create.response.status_code == 200
            assert pre_get.response.status_code == 200

            assert isinstance(pre_create, JsonResponse)
            assert isinstance(pre_get, JsonResponse)
            
            assert pre_get.data.date == pre_date.isoformat()
            assert pre_get.data.from_time == from_time
            assert pre_get.data.to_time == to_time

    def test_getlist(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestPresence.test_getlist"):
            pre_list = self.moco.Presence.getlist(
                from_date=date(2020, 1, 1),
                to_date=date(2021, 1, 1),
                user_id=user.id
            )

            assert pre_list.response.status_code == 200

            assert isinstance(pre_list, ListingResponse)

    def test_update(self):
        with self.recorder.use_cassette("TestPresence.test_update"):
            pre_create = self.moco.Presence.create(
                date(2020, 3, 1),
                "10:30",
                "14:00"
            )

            pre_date = date(2020, 3, 2)
            from_time = "08:00"
            to_time = "09:30"

            pre_update = self.moco.Presence.update(
                pre_create.data.id,
                pres_date=pre_date,
                from_time=from_time,
                to_time=to_time,
            )

            assert pre_create.response.status_code == 200
            assert pre_update.response.status_code == 200

            assert isinstance(pre_create, JsonResponse)
            assert isinstance(pre_update, JsonResponse)

            assert pre_update.data.date == pre_date.isoformat()
            assert pre_update.data.from_time == from_time
            assert pre_update.data.to_time == to_time


    def test_delete(self):
        with self.recorder.use_cassette("TestPresence.test_delete"):
            pre_create = self.moco.Presence.create(
                date(2020, 4, 1),
                "10:00",
                "11:00"
            )

            pre_delete = self.moco.Presence.delete(pre_create.data.id)

            assert pre_create.response.status_code == 200
            assert pre_delete.response.status_code == 204

            assert isinstance(pre_create, JsonResponse)
            assert isinstance(pre_delete, EmptyResponse)

    def test_touch(self):
        with self.recorder.use_cassette("TestPresence.test_touch"):
            pre_touch = self.moco.Presence.touch()

            #touch it a second time to discard it
            pre_sec_touch = self.moco.Presence.touch()

            assert pre_touch.response.status_code == 200
            
            assert isinstance(pre_touch, EmptyResponse)