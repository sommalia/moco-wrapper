from .. import IntegrationTest

from moco_wrapper.util.generator import AccountInternalHourlyRateItemGenerator
from moco_wrapper.util.response import ListResponse, ObjectResponse


class TestAccountInternalHourlyRate(IntegrationTest):
    def get_unit(self):
        with self.recorder.use_cassette("TestAccountInternalHourlyRate.get_unit"):
            return self.moco.Unit.getlist()[0]

    def get_user(self):
        with self.recorder.use_cassette("TestAccountInternalHourlyRate.get_user"):
            return self.moco.User.getlist()[0]

    def test_get(self):
        with self.recorder.use_cassette("TestAccountInternalHourlyRate.test_get"):
            hourly_rate_get = self.moco.AccountInternalHourlyRate.get()

            assert hourly_rate_get.response.status_code == 200

            assert isinstance(hourly_rate_get, ListResponse)

    def test_get_full(self):
        unit = self.get_unit()
        years = [2021, 2020]

        with self.recorder.use_cassette("TestAccountInternalHourlyRate.test_get_full"):
            hourly_rate_get = self.moco.AccountInternalHourlyRate.get(
                years=years,
                unit_id=unit.id
            )

            assert hourly_rate_get.response.status_code == 200

            assert isinstance(hourly_rate_get, ListResponse)

    def test_update(self):
        generator = AccountInternalHourlyRateItemGenerator()

        year = 2020
        user = self.get_user()
        rate = 210.5

        items = [
            generator.generate(user.id, rate)
        ]

        with self.recorder.use_cassette("TestAccountInternalHourlyRate.test_update"):
            rate_update = self.moco.AccountInternalHourlyRate.update(
                year=year,
                rates=items
            )

            assert rate_update.response.status_code == 200

            assert isinstance(rate_update, ObjectResponse)
