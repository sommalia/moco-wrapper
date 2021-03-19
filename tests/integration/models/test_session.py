from moco_wrapper.util.response import ObjectResponse
from moco_wrapper.models.objector_models import SessionVerification


from datetime import date
from .. import IntegrationTest


class TestSession(IntegrationTest):

    def test_verify(self):
        session_verify = self.moco.Session.verify()

        assert session_verify.response.status_code == 200

        assert isinstance(session_verify, ObjectResponse)
        assert isinstance(session_verify.data, SessionVerification)


