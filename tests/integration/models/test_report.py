from moco_wrapper.util.response import ListResponse
from .. import IntegrationTest

class TestReport(IntegrationTest):
    def get_user(self):
        with self.recorder.use_cassette("TestReport.get_user"):
            user = self.moco.User.getlist()[0]
            return user

    def test_absences(self):
        # get user
        user = self.get_user()

        with self.recorder.use_cassette("TestReport.test_absences"):
            # create report
            year = 2022
            active = False
            report_get = self.moco.Report.absences(
                active=active,
                year=year
            )

            assert report_get.response.status_code == 200
            assert isinstance(report_get, ListResponse)
