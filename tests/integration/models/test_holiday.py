from moco_wrapper.util.response import JsonResponse, EmptyResponse, ListingResponse

from .. import IntegrationTest

class TestHolyday(IntegrationTest):
    def get_user(self):
        with self.recorder.use_cassette("TestHoliday.get_user"):
            user = self.moco.User.getlist().items[0]
            return user

    def test_create(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestHoliday.test_create"):
            year = 2019
            title = "last year holiday"
            hours = 2

            holi_create = self.moco.Holiday.create(
                year, 
                title, 
                user.id, 
                hours=hours
            )

            assert holi_create.response.status_code == 200
            
            assert isinstance(holi_create, JsonResponse)

            assert holi_create.data.year == year
            assert holi_create.data.title == title
            assert holi_create.data.hours == hours
            assert holi_create.data.user.id == user.id

    def test_update(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestHoliday.test_update"):
            holi_create = self.moco.Holiday.create(2019, "dummy holiday, test update", user.id)

            year = 2020
            title = "this year holiday"
            hours = 100

            holi_update = self.moco.Holiday.update(
                holi_create.data.id,
                year=year, 
                title=title, 
                user_id=user.id, 
                hours=hours
            )

            assert holi_create.response.status_code == 200
            assert holi_update.response.status_code == 200
            
            assert isinstance(holi_create, JsonResponse)
            assert isinstance(holi_update, JsonResponse)

            assert holi_update.data.year == year
            assert holi_update.data.title == title
            assert holi_update.data.hours == hours
            assert holi_update.data.user.id == user.id

    def test_delete(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestHoliday.test_delete"):
            holi_create = self.moco.Holiday.create(2020, "dummy holiday, test delete", user.id)

            holi_delete = self.moco.Holiday.delete(holi_create.data.id)

            assert holi_create.response.status_code == 200
            assert holi_delete.response.status_code == 204

            assert isinstance(holi_delete, EmptyResponse)

    def test_get(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestHoliday.test_get"):
            year = 2019
            title = "last year holiday"
            hours = 2

            holi_create = self.moco.Holiday.create(
                year, 
                title, 
                user.id, 
                hours=hours
            )

            holi_get = self.moco.Holiday.get(holi_create.data.id)

            assert holi_create.response.status_code == 200
            assert holi_get.response.status_code == 200
            
            assert isinstance(holi_create, JsonResponse)
            assert isinstance(holi_get, JsonResponse)
            
            assert holi_get.data.year == year
            assert holi_get.data.title == title
            assert holi_get.data.hours == hours
            assert holi_get.data.user.id == user.id

    def test_getlist(self):
        with self.recorder.use_cassette("TestHoliday.test_getlist"):
            hol_list = self.moco.Holiday.getlist()

            assert hol_list.response.status_code == 200
            
            assert isinstance(hol_list, ListingResponse)