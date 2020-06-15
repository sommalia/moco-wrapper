import datetime

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH
from enum import Enum
from base64 import b64encode


class PurchaseStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"


class PurchasePaymentMethod(str, Enum):
    BANK_TRANSFER = "bank_transfer"
    DIRECT_DEBIT = "direct_debit"
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    CASH = "cash"


class PurchaseFile(object):
    def __init__(self, filename, base64_content):
        self.filename = filename
        self.base64_content = base64_content

    @classmethod
    def load(cls, path):
        with open(path, "rb") as f:
            return cls(f.name, b64encode(f.read()).decode('utf-8'))


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

    def get(
        self,
        purchase_id: int
    ):
        """
        Retrieve a single purchase

        :param purchase_id: The id of the purchase

        :type purchase_id: int

        :returns: A single purchase
        """
        return self._moco.get(API_PATH["purchase_get"].format(id=purchase_id))

    def create(
        self,
        purchase_date: datetime.date,
        currency: str,
        payment_method: PurchasePaymentMethod,
        items: list,
        due_date: datetime.date = None,
        service_period_from: datetime.date = None,
        service_period_to: datetime.date = None,
        company_id: int = None,
        receipt_identifier: str = None,
        info: str = None,
        iban: str = None,
        reference: str = None,
        custom_properties: dict = None,
        file: PurchaseFile = None,
        tags: list = None
    ):
        """
        Create a new purchase

        :param purchase_date: Date of the purchase
        :param currency: Currency
        :param payment_method: Method of payment that was used
        :param items: List of items that were purchased (minimum 1 item required)
        :param due_date: Date the purchase is due (default ``None``)
        :param service_period_from: Service period start date (default ``None``)
        :param service_period_to: Service period end date (default ``None``)
        :param company_id: Id of the supplier company (default ``None``)
        :param receipt_identifier: Receipt string (default ``None``)
        :param info: Info text (default ``None``)
        :param iban: Iban  (default ``None``)
        :param reference: Reference text (default ``None``)
        :param custom_properties: Custom Properties (default ``None``)
        :param file: File attached to the purchase (default ``None``)
        :param tags: List of tags  (default ``None``)

        :type purchase_date: datetime.date, str
        :type currency: str
        :type payment_method: :class:`.PurchasePaymentMethod`, str
        :type items: List
        :type due_date: datetime.date, str
        :type service_period_from: datetime.date, str
        :type service_period_to: datetime.date, str
        :type company_id: int
        :type receipt_identifier: str
        :type info: str
        :type iban: str
        :type reference: str
        :type custom_properties: dict
        :type file: :class:`.PurchaseFile`
        :type tags: list

        :returns: The created purchase
        """

        data = {
            "date": purchase_date,
            "currency": currency,
            "payment_method": payment_method,
            "items": items,
        }

        if isinstance(data["date"], datetime.date):
            data["date"] = self._convert_date_to_iso(data["date"])

        for key, value in (
            ("due_date", due_date),
            ("service_period_from", service_period_from),
            ("service_period_to", service_period_to),
            ("company_id", company_id),
            ("receipt_identifier", receipt_identifier),
            ("info", info),
            ("iban", iban),
            ("reference", reference),
            ("custom_properties", custom_properties),
            ("file", file),
            ("tags", tags),
        ):
            if value is not None:
                # check if value is a date
                if isinstance(value, datetime.date) and key in ["due_date", "service_period_from", "service_period_to"]:
                    data[key] = self._convert_date_to_iso(value)
                elif isinstance(value, PurchaseFile):  # check if value is a file
                    data[key] = {
                        "filename": value.filename,
                        "base64": value.base64_content
                    }
                else:
                    data[key] = value

        return self._moco.post(API_PATH["purchase_create"], data=data)
