from .. import IntegrationTest
from moco_wrapper.util.response import ListingResponse

class TestPlanningEntry(IntegrationTest):
    def test_getlist(self):
        with self.recorder.use_cassette("TestPlanningEntry.test_getlist"):
            plan_list = self.moco.PlanningEntry.getlist()

            assert plan_list.response.status_code == 200
            assert isinstance(plan_list, ListingResponse)
