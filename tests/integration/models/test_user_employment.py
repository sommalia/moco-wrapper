from moco_wrapper.util.response import PagedListResponse, ObjectResponse

from datetime import date
from .. import IntegrationTest


class TestUserEmployment(IntegrationTest):
    def get_user(self):
        with self.recorder.use_cassette("TestUserEmployment.get_user"):
            user = self.moco.User.getlist()[0]
            return user

    def test_getlist(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestUserEmployment.test_getlist"):
            from_date = date(2020, 1, 1)
            to_date = date(2021, 1, 1)

            emp_list = self.moco.UserEmployment.getlist(
                from_date=from_date,
                to_date=to_date,
                user_id=user.id
            )

            assert emp_list.response.status_code == 200

            assert type(emp_list) is PagedListResponse

            assert emp_list.current_page == 1
            assert emp_list.is_last is not None
            assert emp_list.next_page is not None
            assert emp_list.total is not None
            assert emp_list.page_size is not None

    def test_get(self):
        with self.recorder.use_cassette("TestUserEmployment.test_get"):
            emp_id = self.moco.UserEmployment.getlist()[0].id

            emp_get = self.moco.UserEmployment.get(
                employment_id=emp_id
            )

            assert emp_get.response.status_code == 200

            assert type(emp_get) is ObjectResponse

            assert emp_get.data.user.id is not None
            assert emp_get.data.pattern is not None
            assert emp_get.data.from_date is not None
