from .. import UnitTest


class TestReport(UnitTest):

    def test_absences(self):
        year = 2020
        active = True

        response = self.moco.Report.absences(
            year=year,
            active=active
        )

        params = response["params"]

        assert params["year"] == year
        assert params["active"] == active

        assert response["method"] == "GET"
