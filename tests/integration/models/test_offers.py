from .. import IntegrationTest

from datetime import date

from moco_wrapper.models.offer import OfferStatus
from moco_wrapper.util.response import ListingResponse, JsonResponse, FileResponse, EmptyResponse
from moco_wrapper.util.generator import OfferItemGenerator


class TestOffer(IntegrationTest):

    def get_user(self):
        with self.recorder.use_cassette("TestOffer.get_user"):
            user = self.moco.User.getlist().items[0]
            return user

    def get_deal_category(self):
        with self.recorder.use_cassette("TestOffer.get_deal_category"):
            deal_cat = self.moco.DealCategory.getlist().items[0]

            return deal_cat

    def get_deal(self):
        user = self.get_user()
        deal_cat = self.get_deal_category()

        with self.recorder.use_cassette("TestOffer.get_deal"):
            deal = self.moco.Deal.create(
                "TestOffer Deal",
                "EUR",
                1000,
                date(2020, 1, 1),
                user.id,
                deal_cat.id
            )

            return deal.data

    def get_customer(self):
        with self.recorder.use_cassette("TestOffer.get_customer"):
            customer = self.moco.Company.getlist(company_type="customer").items[0]
            return customer

    def get_project(self):
        leader = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestOffer.get_project"):
            project_create = self.moco.Project.create(
                "project for offer creation",
                "EUR",
                leader.id,
                customer.id,
                finish_date=date(2020, 1, 1),
            )

            return project_create.data

    def get_contact(self):
        with self.recorder.use_cassette("TestOffer.get_contact"):
            contact_create = self.moco.Contact.create("Offer", "Contact", "u")
            return contact_create.data

    def test_getlist(self):
        with self.recorder.use_cassette("TestOffer.test_getlist"):
            off_getlist = self.moco.Offer.getlist()

            assert off_getlist.response.status_code == 200

            assert isinstance(off_getlist, ListingResponse)

            assert off_getlist.current_page == 1
            assert off_getlist.is_last is not None
            assert off_getlist.next_page is not None
            assert off_getlist.total is not None
            assert off_getlist.page_size is not None

    def test_getlist_full(self):
        with self.recorder.use_cassette("TestOffer.test_getlist_full"):
            off_getlist = self.moco.Offer.getlist(status=OfferStatus.ACCEPTED, from_date=date(2020, 1, 1),
                                                  to_date=date(2020, 1, 31), identifier="TEST-IDENT")

            assert off_getlist.response.status_code == 200

            assert isinstance(off_getlist, ListingResponse)

            assert off_getlist.current_page == 1
            assert off_getlist.is_last is not None
            assert off_getlist.next_page is not None
            assert off_getlist.total is not None
            assert off_getlist.page_size is not None

    def test_get(self):
        deal = self.get_deal()
        user = self.get_user()

        with self.recorder.use_cassette("TestOffer.test_get"):
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

            offer_create = self.moco.Offer.create(
                deal.id,
                None,
                rec_address,
                creation_date,
                due_date,
                title,
                tax,
                currency,
                items
            )

            offer_get = self.moco.Offer.get(offer_create.data.id)

            assert offer_create.response.status_code == 201
            assert offer_get.response.status_code == 200

            assert isinstance(offer_create, JsonResponse)
            assert isinstance(offer_get, JsonResponse)

            assert offer_get.data.deal.id == deal.id
            assert offer_get.data.date == creation_date.isoformat()
            assert offer_get.data.due_date == due_date.isoformat()
            assert offer_get.data.title == title
            assert offer_get.data.tax == tax
            assert offer_get.data.currency == currency

    def test_create_from_deal(self):
        deal = self.get_deal()

        with self.recorder.use_cassette("TestOffer.test_create_from_deal"):
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

            offer_create = self.moco.Offer.create(
                deal.id,
                None,
                rec_address,
                creation_date,
                due_date,
                title,
                tax,
                currency,
                items
            )

            assert offer_create.response.status_code == 201

            assert isinstance(offer_create, JsonResponse)

            assert offer_create.data.deal.id == deal.id
            assert offer_create.data.date == creation_date.isoformat()
            assert offer_create.data.due_date == due_date.isoformat()
            assert offer_create.data.title == title
            assert offer_create.data.tax == tax
            assert offer_create.data.currency == currency

    def test_create_with_all_items(self):
        deal = self.get_deal()
        user = self.get_user()

        with self.recorder.use_cassette("TestOffer.test_create_with_all_items"):
            gen = OfferItemGenerator()
            items = [
                gen.generate_title("this is the title"),
                gen.generate_description("This is the first description"),
                gen.generate_detail_postion("support", 1, "h", 65),
                gen.generate_lump_position("server hardware", 200),
                gen.generate_subtotal("subtotal position"),
                gen.generate_detail_postion("special support", 3, "h", 90),
                gen.generate_pagebreak()
            ]

            offer_create = self.moco.Offer.create(
                deal.id,
                None,
                "this is the recipient address",
                date(2020, 1, 1),
                date(2021, 1, 1),
                "offer title",
                19,
                "EUR",
                items
            )

            assert offer_create.response.status_code == 201

            assert isinstance(offer_create, JsonResponse)

            assert len(offer_create.data.items) == 7

    def test_create_with_project(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestOffer.test_create_with_project"):
            rec_address = "this is the recpipient address"
            creation_date = date(2020, 1, 2)
            due_date = date(2021, 1, 1)
            title = "offer created from deal"
            tax = 21.5
            currency = "EUR"

            gen = OfferItemGenerator()
            items = [
                gen.generate_title("offer from project title"),
                gen.generate_lump_position("misc", 2000)
            ]

            offer_create = self.moco.Offer.create(
                None,
                project.id,
                rec_address,
                creation_date,
                due_date,
                title,
                tax,
                currency,
                items
            )

            assert offer_create.response.status_code == 201

            assert isinstance(offer_create, JsonResponse)

            assert offer_create.data.project.id == project.id
            assert offer_create.data.date == creation_date.isoformat()
            assert offer_create.data.title == title
            assert offer_create.data.tax == tax
            assert offer_create.data.currency == currency

    def test_create_full(self):
        project = self.get_project()
        contact = self.get_contact()
        deal = self.get_deal()

        with self.recorder.use_cassette("TestOffer.test_create_full"):
            rec_address = "this is the recpipient address"
            creation_date = date(2020, 1, 2)
            due_date = date(2021, 1, 1)
            title = "offer created from deal"
            tax = 21.5
            currency = "EUR"
            salutation = "salute"
            footer = "footer"
            discount = 20

            gen = OfferItemGenerator()
            items = [
                gen.generate_title("offer from project title"),
                gen.generate_lump_position("misc", 2000)
            ]

            offer_create = self.moco.Offer.create(
                deal.id,
                project.id,
                rec_address,
                creation_date,
                due_date,
                title,
                tax,
                currency,
                items,
                salutation=salutation,
                footer=footer,
                discount=discount,
                contact_id=contact.id
            )

            assert offer_create.response.status_code == 201

            assert isinstance(offer_create, JsonResponse)

            assert offer_create.data.project.id == project.id
            assert offer_create.data.date == creation_date.isoformat()
            assert offer_create.data.title == title
            assert offer_create.data.tax == tax
            assert offer_create.data.currency == currency
            assert offer_create.data.salutation == salutation
            assert offer_create.data.footer == footer
            assert offer_create.data.discount == discount

    def test_pdf(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestOffer.test_pdf"):
            gen = OfferItemGenerator()
            items = [
                gen.generate_title("title"),
                gen.generate_lump_position("pos 1", 200)
            ]

            offer_create = self.moco.Offer.create(None, project.id, "rec address", date(2020, 1, 1), date(2021, 1, 1),
                                                  "title", 21, "EUR", items)
            offer_pdf = self.moco.Offer.pdf(offer_create.data.id)

            assert offer_create.response.status_code == 201
            assert offer_pdf.response.status_code == 200

            assert isinstance(offer_pdf, FileResponse)

    def test_update_status(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestOffer.test_update_status"):
            offer_status = OfferStatus.ACCEPTED

            gen = OfferItemGenerator()
            items = [
                gen.generate_title("title"),
                gen.generate_lump_position("pos 1", 200)
            ]

            offer_create = self.moco.Offer.create(None, project.id, "rec adress", date(2020, 1, 1), date(2021, 1, 1),
                                                  "title", 21, "EUR", items)

            offer_update_status = self.moco.Offer.update_status(offer_create.data.id, offer_status)

            offer_get = self.moco.Offer.get(offer_create.data.id)

            assert offer_create.response.status_code == 201
            assert offer_update_status.response.status_code == 204
            assert offer_get.response.status_code == 200

            assert isinstance(offer_create, JsonResponse)
            assert isinstance(offer_update_status, EmptyResponse)
            assert isinstance(offer_get, JsonResponse)

            assert offer_create.data.status == OfferStatus.CREATED
            assert offer_get.data.status == offer_status
