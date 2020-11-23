from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH


class PurchaseCategory(MWRAPBase):
    """
    Class for handling Purchase Categories.
    """

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

        return self._moco.get(API_PATH["purchase_category_get"].format(id=category_id))

    def getlist(
        self
    ):
        """
        Retrieve a list of categories.

        :returns: List of categories
        :rtype: :class:`moco_wrapper.util.response.ListResponse`
        """

        return self._moco.get(API_PATH["purchase_category_getlist"])
