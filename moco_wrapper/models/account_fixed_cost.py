from typing import List

from moco_wrapper.util.endpoint import Endpoint
from moco_wrapper.models import objector_models as om
from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH


class AccountFixedCost(MWRAPBase):
    """
    Class for handling the fixed costs

    Example Usage:

    .. code-block:: python

        import datetime
        from moco_wrapper import Moco

        m = Moco()

        costs = m.AccountFixedCost.getlist(year=2020)

    """
    @staticmethod
    def endpoints() -> List[Endpoint]:
        """
        Returns all endpoints associated with the model

        :returns: List of Endpoint objects
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`

        """
        return [
            Endpoint("account_fixed_cost_getlist", "/account/fixed_costs", "GET", om.AccountFixedCost),
        ]

    def __init__(self, moco):
        """
        Class constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def getlist(
        self,
        year: int = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1,
    ):
        """
        Retrieve a list of fixed costs

        :param year: The year to retrieve the fixed costs for (default ``None``)
        :param sort_by: Field to the results by (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type year: int
        :type sort_by: str
        :type sort_order: str
        :type page: str

        :returns: List of fixed costs
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`
        """

        params = {}

        for key, value in (
            ("year", year),
            ("page", page)
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get("account_fixed_cost_getlist", params=params)

