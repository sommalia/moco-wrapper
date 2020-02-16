from .base import MWRAPBase
from ..const import API_PATH

from datetime import date
from enum import Enum

class OfferStatus(str, Enum):
    CREATED = "created"
    SENT = "sent"
    ACCEPTED = "accepted"
    BILLED = "billed"
    ARCHIVED = "archived"

class OfferChangeAddress(str, Enum):
    OFFER = "offer"
    CUSTOMER = "customer"

class Offer(MWRAPBase):
    """class for handling offers (in german "angebote")."""

    def __init__(self, moco):
        self._moco = moco

    def getlist(
        self,
        status: OfferStatus = None,
        from_date: date = None,
        to_date: date = None,
        identifier: str = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
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
                if key in ["from", "to"] and isinstance(value, date):
                    params[key] = value.isoformat()
                else:
                    params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["offer_getlist"], params=params)

    def get(
        self,
        id: int
        ):
        """retrieve a sigle offer

        :param id: id of the offer
        :returns: single offer object

        """
        return self._moco.get(API_PATH["offer_get"].format(id=id))

    def pdf(
        self,
        id: int,
        letter_paper_id: int = None
        ):
        """retrive the offer document for a single offer

        :param id: id of the offer
        :param letter_paper_id: id of the letter paper (default white)
        :returns: filestream of the document
        """
        return self._moco.get(API_PATH["offer_pdf"].format(id=id))

    def create(
        self,
        deal_id: int,
        project_id: int,
        recipient_address: str,
        creation_date: date,
        due_date: date,
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
        create a new offer

        :param deal_id: deal id of the offer (either deal id or project id must be specified (or both)), set to null if none is specified
        :param project_id: project id of the offer (either deal id or project id (or both) must be specified), set to null if none is specified
            available types are "project" and "deal"
        :param recipient_address: address of the recipient
        :param creation_date: creation date of the offer
        :param due_date: date the offer is due
        :param title: offer title
        :param tax: offer tax (0.0-100.0)
        :param currency: currency used by the offer ("EUR", "CHF")
        :param items: list of offer items, see OfferItemGenerator
        :param change_address: change offer address propagation, see OfferChangeAdress enum (default offer)
            available values are "offer" and "customer"
        :param salutation: salutation text
        :param footer: footer text
        :param discount: discount in percent
        :param contact_id: id of the contact for the offer
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
            "items": items
        }

        if isinstance(creation_date, date):
            data["date"] = creation_date.isoformat()
        else:
            data["date"] = creation_date

        if isinstance(due_date, date):
            data["due_date"] = due_date.isoformat()
        else:
            data["due_date"] = due_date


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

