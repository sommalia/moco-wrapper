from moco_wrapper.models.schedule import ScheduleAbsenceCode, ScheduleSymbol
from moco_wrapper.models.company import CompanyType
from moco_wrapper.util.response import ObjectResponse, PagedListResponse


from datetime import date
from .. import IntegrationTest


class TestSession(IntegrationTest):

    def test_verify(self):
        session_verify = self.moco.Session.verify()

        assert session_verify.response.status_code == 200



