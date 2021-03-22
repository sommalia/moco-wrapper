from .. import IntegrationTest

from moco_wrapper.util.response import ObjectResponse
from moco_wrapper.models.company import CompanyType


class TestHourlyRate(IntegrationTest):

    def get_customer(self):
        with self.recorder.use_cassette("TestHourlyRate.get_company"):
            company_create = self.moco.Company.create(
                name="TestHourlyRate.get_customer",
                company_type=CompanyType.CUSTOMER
            )

            return company_create.data

    def test_get(self):
        customer = self.get_customer()

        with self.recorder.use_cassette("TestHourlyRate.test_get"):
            hourly_rate_get = self.moco.AccountHourlyRate.get(
                company_id=customer.id
            )

            assert hourly_rate_get.response.status_code == 200

            assert type(hourly_rate_get) is ObjectResponse

            assert hourly_rate_get.data.users is not None
            assert hourly_rate_get.data.tasks is not None
            assert hourly_rate_get.data.defaults_rates is not None
