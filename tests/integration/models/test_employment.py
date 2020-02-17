from moco_wrapper.util.response import ListingResponse, JsonResponse

from datetime import date
from .. import IntegrationTest

class TestEmployment(IntegrationTest):
    def get_user(self):
        with self.recorder.use_cassette("TestEmployment.get_user"):
            user = self.moco.User.getlist().items[0]
            return user

    def test_getlist(self):
        user = self.get_user()

        with self.recorder.use_cassette("TestEmployment.test_getlist"):
            from_date = date(2020, 1, 1)
            to_date = date(2021, 1, 1)
            
            emp_list = self.moco.Employment.getlist(
                from_date, 
                to_date=to_date,
                user_id=user.id
            )

            assert emp_list.response.status_code == 200

            assert isinstance(emp_list, ListingResponse)

    def test_get(self):
        with self.recorder.use_cassette("TestEmployment.test_get"):
            emp_id = self.moco.Employment.getlist().items[0].id

            emp_get = self.moco.Employment.get(emp_id)

            assert emp_get.response.status_code == 200

            assert isinstance(emp_get, JsonResponse)

            assert emp_get.data.user.id is not None
            assert emp_get.data.pattern is not None
            assert emp_get.data.from_date is not None