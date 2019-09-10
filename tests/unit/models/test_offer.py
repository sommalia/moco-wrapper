from .. import UnitTest
import pytest

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

    def test_get(self):
        offer_id = 123

        response = self.moco.Offer.get(offer_id)

        assert response["method"] == "GET"

    def test_get_doc(self):
        offer_id = 123

        response = self.moco.Offer.get_doc(offer_id)

        assert response["method"] == "GET"