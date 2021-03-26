from typing import List

from moco_wrapper.util.endpoint import Endpoint
from moco_wrapper.models import objector_models as om
from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH


class AccountHourlyRate(MWRAPBase):
    """
    Model for handling hourly rates
    """

    @staticmethod
    def endpoints() -> List[Endpoint]:
        """
        Returns all endpoints associated with the model

        :returns: List of Endpoint objects
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`

        """
        return [
            Endpoint("account_hourly_rate_get", "/account/hourly_rates", "GET", om.HourlyRate),
        ]

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def get(
        self,
        company_id: int = None
    ):
        """
        Get the hourly rate

        :param company_id: Company id to get the hourly rates for (default ``None``)

        :type company_id: int

        :returns: Hourly rates of the specified company

        .. note::

            When no company_id is specified the global hourly rates are returned
        """
        params = {}

        for key, value in (
            ("company_id", company_id),
        ):
            if value is not None:
                params[key] = value

        return self._moco.get("account_hourly_rate_get", params=params)
