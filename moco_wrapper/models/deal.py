import datetime

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH

from enum import Enum


class DealStatus(str, Enum):
    """
    Enumeration for the allowed values that can be supplied for the ``status`` argument of :meth:`.Deal.create`,
    :meth:`.Deal.update` and :meth:`.Deal.getlist`.

    .. code-block:: python

        from moco_wrapper.models.deal import DealStatus
        from moco_wrapper import Moco

        m = Moco()

        deal_create = m.Deal.create(
            ..
            status = DealStatus.WON
        )

    """
    POTENTIAL = "potential"
    PENDING = "pending"
    WON = "won"
    LOST = "lost"
    DROPPED = "dropped"


class Deal(MWRAPBase):
    """
    Class for handling deals/leads.
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
        currency: str,
        money: float,
        reminder_date: datetime.date,
        user_id: int,
        deal_category_id: int,
        company_id: int = None,
        info: str = None,
        status: DealStatus = DealStatus.PENDING
    ):
        """
        Create a new deal.

        :param name: Name of the deal
        :param currency: Currency used (e.g. EUR, CHF)
        :param money: How much money can be generated from this deal (e.g. 205.0)
        :param reminder_date: Reminder date
        :param user_id: Id of the user the is responsible for this lead
        :param deal_category_id: Deal category id
        :param company_id: Company id (default ``None``)
        :param info: Additional information (default ``None``)
        :param status: Current state of the deal (default :attr:`.DealStatus.PENDING`)

        :type name: str
        :type currency: str
        :type money: float
        :type reminder_date: datetime.date, str
        :type user_id: int
        :type deal_category_id: int
        :type company_id: int
        :type info: str
        :type status: :class:`.DealStatus`, str

        :returns: The created deal object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """

        data = {
            "name": name,
            "currency": currency,
            "money": money,
            "user_id": user_id,
            "deal_category_id": deal_category_id
        }

        if isinstance(reminder_date, datetime.date):
            data["reminder_date"] = self._convert_date_to_iso(reminder_date)
        else:
            data["reminder_date"] = reminder_date

        for key, value in (
            ("company_id", company_id),
            ("info", info),
            ("status", status)
        ):
            if value is not None:
                data[key] = value

        return self._moco.post(API_PATH["deal_create"], data=data)

    def update(
        self,
        deal_id: int,
        name: str = None,
        currency: str = None,
        money: float = None,
        reminder_date: datetime.date = None,
        user_id: int = None,
        deal_category_id: int = None,
        company_id: int = None,
        info: str = None,
        status: DealStatus = None
    ):
        """
        Update an existing deal.

        :param deal_id: Id of the deal
        :param name: Name of the deal (default ``None``)
        :param currency: Currency used (e.g. EUR, CHF) (default ``None``)
        :param money: How much money can be generated from this deal (e.g. 205.0) (default ``None``)
        :param reminder_date: Reminder date (default ``None``)
        :param user_id: Id of the user that is responsible for this deal (default ``None``)
        :param deal_category_id: Deal category id (default ``None``)
        :param company_id: Company id (default ``None``)
        :param info: Additional information (default ``None``)
        :param status: Current state of the deal (default ``None``)

        :type deal_id: int
        :type name: str
        :type currency: str
        :type money: float
        :type reminder_date: datetime.date, str
        :type user_id: int
        :type deal_category_id: int
        :type company_id: int
        :type info: str
        :type status: :class:`.DealStatus`, str

        :returns: The updated deal object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """

        data = {}
        for key, value in (
            ("name", name),
            ("currency", currency),
            ("money", money),
            ("reminder_date", reminder_date),
            ("user_id", user_id),
            ("deal_category_id", deal_category_id),
            ("company_id", company_id),
            ("info", info),
            ("status", status)
        ):

            if value is not None:
                if key in ["reminder_date"] and isinstance(value, datetime.date):
                    data[key] = self._convert_date_to_iso(value)
                else:
                    data[key] = value

        return self._moco.put(API_PATH["deal_update"].format(id=deal_id), data=data)

    def get(
        self,
        deal_id: int
    ):
        """
        Retrieve a single deal.

        :param deal_id: Id of the deal

        :type deal_id: int

        :returns: Single deal object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        return self._moco.get(API_PATH["deal_get"].format(id=deal_id))

    def getlist(
        self,
        status: str = None,
        tags: list = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Retrieve a list of deal objects.

        :param status: State of deal (default ``None``)
        :param tags: Array of tags (default ``None``)
        :param sort_by: Field to order results by (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type status: :class:`.DealStatus`, str
        :type tags: list
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of deal objects
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`
        """
        params = {}
        for key, value in (
            ("status", status),
            ("tags", tags),
            ("page", page)
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["deal_getlist"], params=params)
