from typing import List

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.util.endpoint import Endpoint
from moco_wrapper.models import objector_models as om


class Session(MWRAPBase):
    """
    Class for handling authentication against the moco api with a users email address and password.

    This model is used internally when the moco instance is created with no api key in the authentication object and
    will be invoked before the first request is fired.
    """

    @staticmethod
    def endpoints() -> List[Endpoint]:
        """
        Returns all endpoints associated with the model

        :returns: List of Endpoint objects
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`

        """
        return [
            Endpoint("session_auth", "/session", "POST", om.SessionAuthentication),
            Endpoint("session_verify", "/session", "GET", om.SessionVerification)
        ]

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self.moco = moco

    def authenticate(
        self,
        email: str,
        password: str
    ):
        """
        Authenticates the client with email and password.

        :param email: Email address
        :param password: Password

        :type email: str
        :type password: str

        :returns: Authentication information
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """

        data = {
            "email": email,
            "password": password
        }

        return self.moco.post("session_auth", data=data, bypass_auth=True)

    def verify(self):
        """
        Verifies that the current api key is still valid

        :returns: Session verification object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """

        return self.moco.get("session_verify")
