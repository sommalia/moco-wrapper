from .. import UnitTest
import pytest

from moco_wrapper.models.offer import OfferCreationBase

class TestOffer(UnitTest):
    def test_getlist(self):
        status = "created"
        from_date = '2019-10-10'
        to_date = '2020-10-10'
        identifier = 'OFFER-10-21'

        response = self.moco.Offer.getlist(status=status, from_date=from_date, to_date=to_date, identifier=identifier)
        params = response["params"]

        assert params["status"] == status
        assert params["from"] == from_date
        assert params["to"] == to_date
        assert params["identifier"] == identifier

        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        sort_by = "field to sort by"

        response = self.moco.Offer.getlist(sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "field to sort by"
        sort_order = "desc"

        response = self.moco.Offer.getlist(sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        page_default = 1

        response = self.moco.Offer.getlist()
        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.Offer.getlist(page=page_overwrite)
        assert response["params"]["page"] == page_overwrite

    def test_get(self):
        offer_id = 123

        response = self.moco.Offer.get(offer_id)

        assert response["method"] == "GET"

    def test_pdf(self):
        offer_id = 123

        response = self.moco.Offer.pdf(offer_id)

        assert response["method"] == "GET"

    def test_create(self):
        deal_id = 1
        recipient_address = "My customer..."
        creation_date = "2018-09-17"
        due_date = "2018-10-16"
        title = "my offer"
        tax = 1.0
        currency = "CHF"
        items = []
        change_address = "offer"
        salutation = "salut"
        footer = "footer text"
        discount = 10.2
        contact_id = 3

        response = self.moco.Offer.create(deal_id, OfferCreationBase.DEAL, recipient_address, creation_date, due_date, title, tax, currency, items, change_address=change_address, salutation=salutation, footer=footer, discount=discount, contact_id=contact_id)

        data = response["data"]

        assert response["method"] == "POST"

        assert data["deal_id"] == deal_id
        assert data["recipient_address"] == recipient_address
        assert data["date"] == creation_date
        assert data["due_date"] == due_date
        assert data["title"] == title
        assert data["tax"] == tax
        assert data["currency"] == currency
        assert data["items"] == items
        assert data["change_address"] == change_address
        assert data["footer"] == footer
        assert data["discount"] == discount
        assert data["contact_id"] == contact_id