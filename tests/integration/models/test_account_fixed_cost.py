from .. import IntegrationTest

from moco_wrapper.util.response import ObjectResponse, PagedListResponse, ListResponse
from moco_wrapper.models.company import CompanyType


class TestAccountFixedCost(IntegrationTest):


    def test_getlist(self):
        year = 2021

        with self.recorder.use_cassette("TestAccountFixedCost.test_getlist"):
            costs_get = self.moco.AccountFixedCost.getlist(
                year=year,
                page=1,
                sort_by="year",
                sort_order="desc"
            )

            assert costs_get.response.status_code == 200

            assert type(costs_get) is PagedListResponse
