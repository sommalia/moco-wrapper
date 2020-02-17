from .. import IntegrationTest

from moco_wrapper.util.response import JsonResponse
from datetime import date

class TestPresence(IntegrationTest):
    def test_create(self):
        with self.recorder.use_cassette("TestPresence.test_create"):
            pres_date = date(2020, 1, 18)
            from_time  = "8:30"
            to_time = "10:30"

            pre_create = self.moco.Presence.create(pres_date, from_time, to_time)
            print (pre_create)
            assert pre_create.response.status_code == 200
            
            assert isinstance(pre_create, JsonResponse)
            
            assert pre_create.data.date == pres_date.isoformat()