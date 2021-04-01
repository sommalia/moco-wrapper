from .. import UnitTest


class TestAccountInternalHourlyRate(UnitTest):

    def test_get_year(self):
        year = 2020
        unit_id = 2

        response = self.moco.AccountInternalHourlyRate.get(
            years=year,
            unit_id=unit_id
        )

        params = response["params"]

        assert params["years"] == year
        assert params["unit_id"] == unit_id

    def test_get_years(self):
        years = [123, 1234]
        years_expected = ",".join([str(x) for x in years])
        unit_id = 4

        response = self.moco.AccountInternalHourlyRate.get(
            years=years,
            unit_id=unit_id
        )

        params = response["params"]

        assert params["years"] == years_expected
        assert params["unit_id"] == unit_id

        assert response["method"] == "GET"
