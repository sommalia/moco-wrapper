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
        self,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Retrieve a list of categories.

        :param sort_by: Sort by field (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of categories
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`
        """

        params = {
            "page": page
        }

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["purchase_category_getlist"], params=params)
