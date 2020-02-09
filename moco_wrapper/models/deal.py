from .base import MWRAPBase
from ..const import API_PATH

from enum import Enum
from datetime import date

class DealStatus(str, Enum):
    POTENTIAL = "potential"
    PENDING = "pending"
    WON = "won"
    LOST = "lost"
    DROPPED = "dropped"


class Deal(MWRAPBase):
    """Class for handling leads"""

    def __init__(self, moco):
        self._moco = moco

    def create(
        self,
        name: str,
        currency: str,
        money: float,
        reminder_date: date,
        user_id: int,
        deal_category_id: int,
        company_id: int = None,
        info: str = None,
        status: str = "pending"
        ):
        """create a new lead

        :param name: name of the lead
        :param currency: currency used (EUR, CHF)
        :param money: how much money is in this lead (ie 205.0)
        :param reminder_date: reminder date (format YYYY-MM-DD)
        :param user_id: user id that is responsible for this lead
        :param deal_category_id: deal category id
        :param company_id: company id
        :param info: addtionnal information
        :param status: "potential", "pending", "won", "lost" or "dropped" (default: "pending")
        :returns: the created lead object
        """
        
        data = {
            "name": name,
            "currency" : currency,
            "money": money,
            "user_id" : user_id,
            "deal_category_id": deal_category_id
        }

        if isinstance(reminder_date, date):
            data["reminder_date"] = reminder_date.isoformat()
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
        id: int,
        name: str = None,
        currency: str = None,
        money: float = None,
        reminder_date: date = None,
        user_id: int = None,
        deal_category_id: int = None,
        company_id: int = None,
        info: str = None,
        status: DealStatus = None
        ):
        """update a new lead
        :param id: id of the lead
        :param name: name of the lead
        :param currency: currency used (EUR)
        :param money: how much money is in this lead (ie 205.0)
        :param reminder_date: reminder date (format YYYY-MM-DD)
        :param user_id: user id that is responsible for this lead
        :param deal_category_id: deal category id
        :param company_id: company id
        :param info: addtionnal information
        :param status: "potential", "pending", "won", "lost" or "dropped" (default: "pending")
        :returns: the created lead object
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
                if key in ["reminder_date"] and isinstance(value, date):
                    data[key] = value.isoformat()
                else:
                    data[key] = value

        return self._moco.put(API_PATH["deal_update"].format(id=id), data=data)


    def get(
        self,
        id: int
        ):
        """retrieve a single lead

        :param id: id of the lead
        :returns: lead object

        """
        return self._moco.get(API_PATH["deal_get"].format(id=id))

    def getlist(
        self,
        status: str = None,
        tags: list = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
        ):
        """retrieve a list of leads

        :param status: status of the leads ("potential", "pending", "won", "lost" or "dropped")
        :param tags: array of tags
        :param sort_by: field to order results by
        :param sort_order: asc or desc (default asc)
        :param page: page number (default 1)
        :returns: list of deal objects
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

    