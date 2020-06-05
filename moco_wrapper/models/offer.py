import datetime

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH

from enum import Enum


class OfferStatus(str, Enum):
    """
    Enumeration for allowed values of the ``status`` argument of :meth:`.Offer.getlist`.

    Example usage:

    .. code-block:: python

        from moco_wrapper.models.offer import OfferStatus
        from moco_wrapper import Moco

        m = Moco()
        sent_offers = m.Offer.getlist(
            ..
            status = OfferStatus.SENT
        )
    """
    CREATED = "created"
    SENT = "sent"
    ACCEPTED = "accepted"
    BILLED = "billed"
    ARCHIVED = "archived"
    PARTIALLY_BILLED = "partially_billed"


class OfferChangeAddress(str, Enum):
    """
    Enumeration for allowed values of the ``change_address`` argument of :meth:`.Offer.create`.

    Example usage:

    .. code-block:: python

        from moco_wrapper.models.offer import OfferChangeAddress
        from moco_wrapper import Moco

        m = Moco()
        new_offer = m.Offer.create(
            ..
            change_address = OfferChangeAddress.CUSTOMER
        )
    """
    OFFER = "offer"
    CUSTOMER = "customer"


class Offer(MWRAPBase):
    """
    Class for handling offers.
    """

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def getlist(
        self,
        status: OfferStatus = None,
        from_date: datetime.date = None,
        to_date: datetime.date = None,
        identifier: str = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Retrieve a list of offers.

        :param status: State the offer is in
        :param from_date: Start date
        :param to_date: End date
        :param identifier: Identifier string (e.g.: "A1903-003")
        :param sort_by: Field to sort the results by
        :param sort_order: asc or desc (default asc)
        :param page: Page number (default 1)

        :type status: :class:`.OfferStatus`, str
        :type from_date: datetime.date, str
        :type to_date: datetime.date, str
        :type identifier: str
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of offer objects


        .. note::
            Offers can be sorted by ``date``, ``created_at`` and ``title``.
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
                if key in ["from", "to"] and isinstance(value, datetime.date):
                    params[key] = self._convert_date_to_iso(value)
                else:
                    params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["offer_getlist"], params=params)

    def get(
        self,
        offer_id: int
    ):
        """
        Retrieve a single offer.

        :param offer_id: Id of the offer

        :type offer_id: int

        :returns: Single offer object
        """
        return self._moco.get(API_PATH["offer_get"].format(id=offer_id))

    def pdf(
        self,
        offer_id: int,
        letter_paper_id: int = None
    ):
        """
        Retrieve the offer document for a single offer.

        :param offer_id: Id of the offer
        :param letter_paper_id: Id of the letter paper (default white)

        :type offer_id: int
        :type letter_paper_id: int

        :returns: The offers pdf document
        """
        return self._moco.get(API_PATH["offer_pdf"].format(id=offer_id))

    def create(
        self,
        deal_id: int,
        project_id: int,
        recipient_address: str,
        creation_date: datetime.date,
        due_date: datetime.date,
        title: str,
        tax: float,
        currency: str,
        items: list,
        change_address: OfferChangeAddress = OfferChangeAddress.OFFER,
        salutation: str = None,
        footer: str = None,
        discount: float = None,
        contact_id: int = None
    ):
        """
        Create a new offer.

        :param deal_id: Deal id of the offer
        :param project_id: project id of the offer
        :param recipient_address: Address of the recipient (e.g. Test Custmer\\\\nMain Street 5\\\\nExample Town)
        :param creation_date: Creation date
        :param due_date: Date the offer is due
        :param title: Title of the offer
        :param tax: Tax (0.0-100.0)
        :param currency: Currency code used (e.g. EUR, CHF)
        :param items: List of offer items
        :param change_address: change offer address propagation
        :param salutation: Salutation text
        :param footer: Footer text
        :param discount: Discount in percent
        :param contact_id: Id of the contact for the offer

        :type deal_id: int
        :type project_id: int
        :type recipient_address: str
        :type creation_date: datetime.date, str
        :type due_date: datetime.date, str
        :type title: str
        :type tax: float
        :type currency: str
        :type items: list
        :type change_address: :class:`.OfferChangeAddress`, str
        :type salutation: str
        :type footer: str
        :type discount: float
        :type contact_id: int

        :returns: The created offer

        .. note::
            Either ``deal_id`` or ``project_id`` must be specified (or both)

        .. seealso::
            :class:`moco_wrapper.util.generator.OfferItemGenerator`
        """

        if project_id is None and deal_id is None:
            raise ValueError("Either deal_id or project_id (or both) must be specified")

        data = {
            "deal_id": deal_id,
            "project_id": project_id,
            "recipient_address": recipient_address,
            "title": title,
            "tax": tax,
            "currency": currency,
            "items": items,
            "date": creation_date,
            "due_date": due_date,
        }

        for date_key in ["date", "due_date"]:
            if isinstance(data[date_key], datetime.date):
                data[date_key] = self._convert_date_to_iso(data[date_key])

        for key, value in (
            ("change_address", change_address),
            ("salutation", salutation),
            ("footer", footer),
            ("discount", discount),
            ("contact_id", contact_id)
        ):
            if value is not None:
                data[key] = value

        return self._moco.post(API_PATH["offer_create"].format(id=id), data=data)

    def update_status(
        self,
        offer_id,
        status,
    ):
        """
        Updates the state of an offer

        :param offer_id: Id of the offer
        :param status: The new state for the offer

        :type offer_id: int
        :type status: :class:`.OfferStatus`, str

        :returns: Empty response on success
        """
        data = {
            "status": status
        }

        return self._moco.put(API_PATH["offer_update_status"].format(id=offer_id), data=data)
