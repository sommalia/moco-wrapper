from typing import List, Union

from moco_wrapper.util.endpoint import Endpoint
from moco_wrapper.models import objector_models as om
from .base import MWRAPBase


class AccountInternalHourlyRate(MWRAPBase):
    """
    Model for working with the internal rates of the account
    """

    @staticmethod
    def endpoints() -> List[Endpoint]:
        """
        Returns all endpoints associated with the model

        :returns: List of Endpoint objects
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`

        """
        return [
            Endpoint("account_internal_hourly_rate_get", "/account/internal_hourly_rates",
                     "GET", om.AccountInternalHourlyRate),
            Endpoint("account_internal_hourly_rate_update", "/account/internal_hourly_rates",
                     "PATCH")
        ]

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def get(
        self,
        years: Union[int, List[int]] = None,
        unit_id: int = None
    ):
        """
        Retrieve internal hourly rates

        :param years: Single year or list of years
        :param unit_id: Id of the unit

        :type years: int, list
        :type unit_id: int

        :returns: List of internal rates
        :rtype: :class:`moco_wrapper.util.response.ListResponse`
        """

        params = {}
        for key, value in (
            ("years", years),
            ("unit_id", unit_id)
        ):
            if value is not None:
                if key in ["years"] and isinstance(value, list):
                    params[key] = ",".join([str(x) for x in value])
                else:
                    params[key] = value

        return self._moco.get("account_internal_hourly_rate_get", params=params)

    def update(
        self,
        year: int,
        rates : List[dict]
    ):
        """
        Update internal rates

        :param year: Year to update the internal rates for
        :param rates: List of rate objects (each object containing user_id and a rate)

        :type year: int
        :type rates: list

        :returns: Status message on success (can be ignored)
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`

        .. note::

            For generating items see :class:`moco_wrapper.util.generator.AccountInternalRateItemGenerator`

        .. note::

            On success the dictionary `{ "status": "ok" }` will be returned.
            The response can safely be ignored.

        """

        data = {
            "year": year,
            "rates": rates
        }

        return self._moco.patch("account_internal_hourly_rate_update", data=data)




