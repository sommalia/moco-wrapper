from .base import MWRAPBase
from ..const import API_PATH

from enum import Enum
from datetime import date

class DealCategory(MWRAPBase):
    """
    Model for handling the different deal_categories used by the deal model. In German "Akquise-Stufen"
    """

    def __init__(self, moco):
        self._moco = moco

    def create(
        self, 
        name: str,
        probability: int
        ):
        """create a new deal category

        :param name: name of the deal category
        :param probability: probality in (between 0 and 100)
        :returns: the created deal category
        """

        data = {
            "name" : name,
            "probability": probability
        }

        return self._moco.post(API_PATH["deal_category_create"], data=data)

    def update(
        self,
        id: int,
        name: str = None,
        probability: int = None
        ):
        """updates an existing deal category

        :param id: id of the deal category to update
        :param name: name of the deal category
        :param probability: probality in (between 0 and 100)
        :returns: the updated deal category
        """
        data = {}

        for key, value in (
            ("name", name),
            ("probability", probability)
        ):
            if value is not None:
                data[key] = value

        return self._moco.put(API_PATH["deal_category_update"].format(id=id), data=data)


    def getlist(
        self,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
        ):
        """retrieves a list of a deal categories

        :param sort_by: field to sort by 
        :param sort_order: asc or desc (default asc)
        :param page: page number (default 1)
        :returns: list of deal cateogories
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
        id: int
        ):
        """retrieves a single deal category

        :param id: id of the deal category to retrieve
        :returns: single deal category
        """

        return self._moco.get(API_PATH["deal_category_get"].format(id=id))

    def delete(
        self,
        id: int
        ):
        """delete a deal category

        :param id: id of the deal category to delete
        """

        return self._moco.delete(API_PATH["deal_category_delete"].format(id=id))

