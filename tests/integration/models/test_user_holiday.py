from moco_wrapper.util.response import ObjectResponse, EmptyResponse, PagedListResponse

from .. import IntegrationTest

class TestUserHoliday(IntegrationTest):
    def get_user(self):
        with self.recorder.use_cassette("TestUserHoliday.get_user"):
            user = self.moco.User.getlist().items[0]
            return user

    def test_create(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestUserHoliday.test_create"):
            year = 2019
            title = "last year holiday"
            hours = 2

            holi_create = self.moco.UserHoliday.create(
                year, 
                title, 
                user.id, 
                hours=hours
            )

            assert holi_create.response.status_code == 200
            
            assert type(holi_create) is ObjectResponse

            assert holi_create.data.year == year
            assert holi_create.data.title == title
            assert holi_create.data.hours == hours
            assert holi_create.data.user.id == user.id

    def test_create_with_days(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestUserHoliday.test_create_with_days"):
            year = 2019
            title = "dummy holiday, (test create with days)"
            days = 2

            holi_create = self.moco.UserHoliday.create(
                year,
                title,
                user.id,
                days=days
            )

            assert holi_create.response.status_code == 200
            
            assert type(holi_create) is ObjectResponse

            assert holi_create.data.year == year
            assert holi_create.data.title == title
            assert holi_create.data.days == days
            assert holi_create.data.user.id == user.id


    def test_update(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestUserHoliday.test_update"):
            holi_create = self.moco.UserHoliday.create(
                2019, 
                "dummy holiday, test update", 
                user.id, 
                hours=0
            )

            year = 2020
            title = "this year holiday"
            hours = 100

            holi_update = self.moco.UserHoliday.update(
                holi_create.data.id,
                year=year, 
                title=title, 
                user_id=user.id, 
                hours=hours
            )

            assert holi_create.response.status_code == 200
            assert holi_update.response.status_code == 200
            
            assert type(holi_create) is ObjectResponse
            assert type(holi_update) is ObjectResponse

            assert holi_update.data.year == year
            assert holi_update.data.title == title
            assert holi_update.data.hours == hours
            assert holi_update.data.user.id == user.id

    def test_update_with_days(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestUserHoliday.test_update_with_days"):
            holi_create = self.moco.UserHoliday.create(
                2019, 
                "dummy holiday, test update (with days)", 
                user.id, 
                days=1)

            year = 2020
            title = "this year holiday"
            days = 3

            holi_update = self.moco.UserHoliday.update(
                holi_create.data.id,
                year=year, 
                title=title, 
                user_id=user.id, 
                days=days
            )

            assert holi_create.response.status_code == 200
            assert holi_update.response.status_code == 200
            
            assert type(holi_create) is ObjectResponse
            assert type(holi_update) is ObjectResponse

            assert holi_update.data.year == year
            assert holi_update.data.title == title
            assert holi_update.data.days == days
            assert holi_update.data.user.id == user.id

    def test_delete(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestUserHoliday.test_delete"):
            holi_create = self.moco.UserHoliday.create(2020, "dummy holiday, test delete", user.id, hours=0)

            holi_delete = self.moco.UserHoliday.delete(holi_create.data.id)

            assert holi_create.response.status_code == 200
            assert holi_delete.response.status_code == 204

            assert type(holi_delete) is EmptyResponse

    def test_get(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestUserHoliday.test_get"):
            year = 2019
            title = "last year holiday"
            hours = 2

            holi_create = self.moco.UserHoliday.create(
                year, 
                title, 
                user.id, 
                hours=hours
            )

            holi_get = self.moco.UserHoliday.get(holi_create.data.id)

            assert holi_create.response.status_code == 200
            assert holi_get.response.status_code == 200
            
            assert type(holi_create) is ObjectResponse
            assert type(holi_get) is ObjectResponse
            
            assert holi_get.data.year == year
            assert holi_get.data.title == title
            assert holi_get.data.hours == hours
            assert holi_get.data.user.id == user.id

    def test_getlist(self):
        with self.recorder.use_cassette("TestUserHoliday.test_getlist"):
            hol_list = self.moco.UserHoliday.getlist()

            assert hol_list.response.status_code == 200
            
            assert type(hol_list) is PagedListResponse

            assert hol_list.current_page == 1
            assert hol_list.is_last is not None
            assert hol_list.next_page is not None
            assert hol_list.total is not None
            assert hol_list.page_size is not None
            