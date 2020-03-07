from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH

from enum import Enum

class DealCategory(MWRAPBase):
    """
    Model for handling the different deal_categories used by a pending deal.

    A deal (see :class:`moco_wrapper.models.Deal`) that is in the state ``PENDING`` (see :class:`moco_wrapper.models.deal.DealStatus`) must be assigned to deal category. A category has a name and a probability of success (in percent). 

    Typicly a deal that is in ``PENDING`` starts at 1% and moves into the state ``WON`` if the probability reaches 100%.
    
    .. code-block:: python

        from moco_wrapper import Moco

        m = Moco()

        #create a category with 75% success probability
        new_category = m.DealCategory.create(
            "Second round of negotiation",
            75
        ) 

    """

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def create(
        self, 
        name: str,
        probability: int
        ):
        """
        Create a new deal category.

        :param name: Name of the deal category (must be unique)
        :param probability: Deal category success probability (between 1 and 100)

        :type name: str
        :type probability: int
        
        :returns: The created deal category
        """

        data = {
            "name" : name,
            "probability": probability
        }

        return self._moco.post(API_PATH["deal_category_create"], data=data)

    def update(
        self,
        category_id: int,
        name: str = None,
        probability: int = None
        ):
        """
        Updates an existing deal category.

        :param category_id: Id of the deal category to update
        :param name: Name of the deal category (must be unique)
        :param probability: Deal category success probability (between 1 and 100)

        :type category_id: int
        :type name: str
        :type probability: int

        :returns: The updated deal category
        """
        data = {}

        for key, value in (
            ("name", name),
            ("probability", probability)
        ):
            if value is not None:
                data[key] = value

        return self._moco.put(API_PATH["deal_category_update"].format(id=category_id), data=data)


    def getlist(
        self,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
        ):
        """
        Retrieves a list of a deal categories.

        :param sort_by: Field to sort by 
        :param sort_order: asc or desc (default asc)
        :param page: Page number (default 1)

        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of deal categories
        """
        params = {}
        for key, value in (
            ("page", page),
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["deal_category_getlist"], params=params)

    def get(
        self,
        category_id: int
        ):
        """
        Retrieves a single deal category.

        :param category_id: Id of the deal category to retrieve

        :type category_id: int

        :returns: Single deal category
        """

        return self._moco.get(API_PATH["deal_category_get"].format(id=category_id))

    def delete(
        self,
        category_id: int
        ):
        """
        Delete a deal category.

        :param category_id: Id of the deal category to delete

        :type category_id: int

        :reuturns: Empty response on success
        """

        return self._moco.delete(API_PATH["deal_category_delete"].format(id=category_id))

