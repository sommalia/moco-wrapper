from .. import IntegrationTest

from datetime import date

from moco_wrapper.models.offer import OfferStatus
from moco_wrapper.util.response import ListingResponse, JsonResponse, FileResponse

class TestOffer(IntegrationTest):

    def test_getlist(self):
        with self.recorder.use_cassette("TestOffer.test_getlist"):
            off_getlist = self.moco.Offer.getlist()

            assert off_getlist.response.status_code == 200
            
            assert isinstance(off_getlist, ListingResponse)

    def test_getlist_full(self):
        with self.recorder.use_cassette("TestOffer.test_getlist_full"):
            off_getlist = self.moco.Offer.getlist(status=OfferStatus.ACCEPTED, from_date=date(2020, 1, 1), to_date=date(2020, 1, 31), identifier="TEST-IDENT") 
            
            assert off_getlist.response.status_code == 200

            assert isinstance(off_getlist, ListingResponse)

    def test_get(self):
        pass
    