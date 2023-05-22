import time

import pytest

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
        user = self.get_user()

        with self.recorder.use_cassette("TestUserEmployment.test_get"):
            self.cleanup_employments(user.id)

            emp_create = self.moco.UserEmployment.create(
                user_id=user.id,
                pattern={
                    "am": [1,1,1,1,1],
                    "pm": [1,1,1,1,1]
                },
                from_date="2020-01-01",
                to_date="2021-12-31"
            )

            emp_get = self.moco.UserEmployment.get(
                employment_id=emp_create.data.id
            )

            assert emp_get.response.status_code == 200

            assert type(emp_get) is ObjectResponse

            assert emp_get.data.user.id is not None
            assert emp_get.data.pattern is not None
            assert emp_get.data.from_date is not None


    def test_create(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestUserEmployment.test_create"):
            self.cleanup_employments(user.id)

            pattern = {
                "am": [2,2,2,2,2],
                "pm": [2,2,2,2,2]
            }

            from_date = date(2020, 2, 1)
            to_date = date(2020, 2, 10)

            emp_create = self.moco.UserEmployment.create(
                user_id=user.id,
                pattern=pattern,
            )

            assert emp_create.response.status_code == 200



    def cleanup_employments(self, user_id):
        # cleanup all employments of the user
        items = self.moco.UserEmployment.getlist().items
        for e in items:
            print(e)
            self.moco.UserEmployment.delete(e.id)
