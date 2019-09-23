from .base import MWRAPBase
from ..const import API_PATH

class Offer(MWRAPBase):
    """class for handling offers (in german "angebote")."""

    def __init__(self, moco):
        self._moco = moco

    def getlist(
        self,
        status = None,
        from_date = None,
        to_date = None,
        identifier = None,
        sort_by = None,
        sort_order = 'asc',
        page = 1
        ):
        """retrieve a list of offers

        :param status: offer status ("created", "sent", "accepted", "billed", "archived")
        :param from_date: starting filter date (format YYYY-MM-DD)
        :param to_date: ending filter date (format YYYY-MM-DD)
        :param identifier: offer identifier string (ex: "A1903-003")
        :param sort_by: field to sort the results by
        :param sort_order: asc or desc (default asc)
        :param page: page number (default 1)
        :returns: list of offer objects
        """
        params = {}
        for key, value in (
            ("status", status),
            ("from", from_date),
            ("to", to_date),
            ("identifier", identifier),
            ("page", page),
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["offer_getlist"], params=params)

    def get(
        self,
        id
        ):
        """retrieve a sigle offer

        :param id: id of the offer
        :returns: single offer object

        """
        return self._moco.get(API_PATH["offer_get"].format(id=id))

    def get_doc(
        self,
        id,
        letter_paper_id = None
        ):
        """retrive the offer document for a single offer

        :param id: id of the offer
        :param letter_paper_id: id of the letter paper (default white)
        :returns: filestream of the document
        """
        return self._moco.get(API_PATH["offer_get_doc"].format(id=id))