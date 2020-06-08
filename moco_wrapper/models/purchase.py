import datetime

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH
from enum import Enum


class PurchaseStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"


class Purchase(MWRAPBase):

    def __init__(self, moco):
        """
        Class constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def getlist(
        self,
        purchase_id: int = None,
        category_id: int = None,
        term: str = None,
        company_id: int = None,
        status: PurchaseStatus = None,
        tags: list = None,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
        unpaid: bool = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Retrieve a list of purchases

        :param purchase_id: Id of the purchase (default ``None``)
        :param category_id: Id of the category the purchase belongs to  (default ``None``)
        :param term: Full text search  (default ``None``)
        :param company_id: Company id of the supplier (default ``None``)
        :param status: Status of the purchases, see :class:`.PurchaseStatus`
        :param tags: List of tags (default ``None``)
        :param start_date: Start date filter (if ``start_date`` is supplied, ``end_date`` must also be supplied) (default ``None``)
        :param end_date: End date filter (if ``end_date`` is supplied, ``start_date`` must also be supplied) (default ``None``)
        :param unpaid: Filter only purchases without a payment (default ``None``)
        :param sort_by: Field to sort results by (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type purchase_id: int
        :type category_id: int
        :type term: str
        :type company_id: int
        :type status: :class:`.PurchaseStatus`, str
        :type tags: list
        :type start_date: datetime.date, str
        :type end_date: datetime.date, str
        :type unpaid: bool
        :type sort_by: str
        :type sort_order: str
        :type page: int
        """

        if start_date is not None and end_date is None:
            raise ValueError("If start_date is set, so must be end_date")

        if end_date is not None and start_date is None:
            raise ValueError("If end_date is set, so must be start_date")

        params = {}

        if start_date is not None and end_date is not None:
            start_date_formatted = ""
            if isinstance(start_date, datetime.date):
                start_date_formatted = self._convert_date_to_iso(start_date)
            else:
                start_date_formatted = start_date

            end_date_formatted = ""
            if isinstance(end_date, datetime.date):
                end_date_formatted = self._convert_date_to_iso(end_date)
            else:
                end_date_formatted = end_date

            params["date"] = "{}:{}".format(start_date_formatted, end_date_formatted)

        for key, value in (
            ("id", purchase_id),
            ("category_id", category_id),
            ("term", term),
            ("company_id", company_id),
            ("status", status),
            ("tags", tags),
            ("unpaid", unpaid),
            ("page", page)
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["purchase_getlist"], params=params)
