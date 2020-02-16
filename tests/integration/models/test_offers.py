from .. import IntegrationTest

from datetime import date

from moco_wrapper.models.offer import OfferStatus, OfferCreationBase
from moco_wrapper.util.response import ListingResponse, JsonResponse, FileResponse
from moco_wrapper.util.generator import OfferItemGenerator

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
        with self.recorder.use_cassette("TestOffer.test_get"):
            user_id = self.moco.User.getlist().items[0].id
            deal_category_id = self.moco.DealCategory.getlist().items[0].id
            deal_create = self.moco.Deal.create("deal to create offer from", "EUR", 200, date(2020, 1, 1), user_id, deal_category_id)

            offer_base_type = OfferCreationBase.DEAL
            rec_address = "this is the recpipient address"
            creation_date = date(2020, 1, 2)
            due_date = date(2021, 1, 1)
            title = "offer created from deal"
            tax = 21.5
            currency = "EUR"


            gen = OfferItemGenerator()
            items = [
                gen.generate_title("This is the title of the offer"),
                gen.generate_description("this is the description"),
                gen.generate_item("MailChimp Einrichtung", quantity=1, unit="h", unit_price=100.0, net_total=400),
                gen.generate_item("On Site Support", quantity=20, unit_price=20, unit="h", net_total=400, optional=True)
            ]

            offer_create = self.moco.Offer.create(deal_create.data.id, OfferCreationBase.DEAL, rec_address, creation_date, due_date, title, tax, currency, items)

            offer_get = self.moco.Offer.get(offer_create.data.id)

            assert deal_create.response.status_code == 200
            assert offer_create.response.status_code == 201
            assert offer_get.response.status_code == 200

            assert isinstance(offer_create, JsonResponse)
            assert isinstance(offer_get, JsonResponse)

            assert offer_get.data.deal.id == deal_create.data.id
            assert offer_get.data.date == creation_date.isoformat()
            assert offer_get.data.due_date == due_date.isoformat()
            assert offer_get.data.title == title
            assert offer_get.data.tax == tax
            assert offer_get.data.currency == currency

    
    def test_create_from_deal(self):
        with self.recorder.use_cassette("TestOffer.test_create_from_deal"):
            user_id = self.moco.User.getlist().items[0].id
            deal_category_id = self.moco.DealCategory.getlist().items[0].id
            deal_create = self.moco.Deal.create("deal to create offer from", "EUR", 200, date(2020, 1, 1), user_id, deal_category_id)

            offer_base_type = OfferCreationBase.DEAL
            rec_address = "this is the recpipient address"
            creation_date = date(2020, 1, 2)
            due_date = date(2021, 1, 1)
            title = "offer created from deal"
            tax = 21.5
            currency = "EUR"


            gen = OfferItemGenerator()
            items = [
                gen.generate_title("This is the title of the offer"),
                gen.generate_description("this is the description"),
                gen.generate_item("MailChimp Einrichtung", quantity=1, unit="h", unit_price=100.0, net_total=400),
                gen.generate_item("On Site Support", quantity=20, unit_price=20, unit="h", net_total=400, optional=True)
            ]


            offer_create = self.moco.Offer.create(deal_create.data.id, OfferCreationBase.DEAL, rec_address, creation_date, due_date, title, tax, currency, items)

            assert deal_create.response.status_code == 200
            assert offer_create.response.status_code == 201

            assert isinstance(offer_create, JsonResponse)

            assert offer_create.data.deal.id == deal_create.data.id
            assert offer_create.data.date == creation_date.isoformat()
            assert offer_create.data.due_date == due_date.isoformat()
            assert offer_create.data.title == title
            assert offer_create.data.tax == tax
            assert offer_create.data.currency == currency

    def test_create_with_shortcut_items(self):
        with self.recorder.use_cassette("TestOffer.test_create_with_shortcut_items"):
            user_id = self.moco.User.getlist().items[0].id
            deal_category_id = self.moco.DealCategory.getlist().items[0].id
            deal_create = self.moco.Deal.create("deal to create offer from", "EUR", 200, date(2020, 1, 1), user_id, deal_category_id)

            offer_base_type = OfferCreationBase.DEAL
            rec_address = "this is the recpipient address"
            creation_date = date(2020, 1, 2)
            due_date = date(2021, 1, 1)
            title = "offer created from deal"
            tax = 21.5
            currency = "EUR"


            gen = OfferItemGenerator()
            items = [
                gen.generate_title("This is the title of the offer"),
                gen.generate_description("this is the description"),
                gen.generate_detail_postion("MailChimp Einrichtung", quantity=1, unit="h", unit_price=100.0),
                gen.generate_detail_postion("On Site Support", quantity=20, unit_price=20, unit="h", optional=True),
                gen.generate_separator(),
                gen.generate_lump_position("Server XXX-1", 4000.00, optional=False)
            ]


            offer_create = self.moco.Offer.create(deal_create.data.id, OfferCreationBase.DEAL, rec_address, creation_date, due_date, title, tax, currency, items)

            assert deal_create.response.status_code == 200
            assert offer_create.response.status_code == 201

            assert isinstance(offer_create, JsonResponse)