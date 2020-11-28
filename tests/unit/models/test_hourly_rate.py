from .. import UnitTest


class TestHourlyRate(UnitTest):

    def test_get(self):
        company_id = 2

        response = self.moco.HourlyRate.get(
            company_id=company_id
        )

        params = response["params"]

        assert params["company_id"] == company_id

        assert response["method"] == "GET"
