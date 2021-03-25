from typing import List

from moco_wrapper.util.endpoint import Endpoint
from moco_wrapper.models import objector_models as om
from moco_wrapper.models.base import MWRAPBase


class PurchaseCategory(MWRAPBase):
    """
    Class for handling Purchase Categories.
    """

    @staticmethod
    def endpoints() -> List[Endpoint]:
        """
        Returns all endpoints associated with the model

        :returns: List of Endpoint objects
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`

        """
        return [
            Endpoint("purchase_category_get", "/purchases/categories/{id}", "GET", om.PurchaseCategory),
            Endpoint("purchase_category_getlist", "/purchases/categories", "GET", om.PurchaseCategory)
        ]

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def get(
        self,
        category_id: int
    ):
        """
        Retrieve a single category.

        :param category_id: Id of the category to retrieve

        :type category_id: int

        :returns: Single Category object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """

        ep_params = {
            "id": category_id
        }
        return self._moco.get("purchase_category_get", ep_params=ep_params)

    def getlist(
        self
    ):
        """
        Retrieve a list of categories.

        :returns: List of categories
        :rtype: :class:`moco_wrapper.util.response.ListResponse`
        """

        return self._moco.get("purchase_category_getlist")
