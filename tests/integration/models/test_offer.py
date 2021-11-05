from .. import IntegrationTest

from datetime import date

from moco_wrapper.models.offer import OfferStatus
from moco_wrapper.models.contact import ContactGender
from moco_wrapper.util.response import PagedListResponse, ObjectResponse, FileResponse, EmptyResponse
from moco_wrapper.util.generator import OfferItemGenerator


class TestOffer(IntegrationTest):

    def get_user(self):
        with self.recorder.use_cassette("TestOffer.get_user"):
            user = self.moco.User.getlist()[0]
            return user

    def get_deal_category(self):
        with self.recorder.use_cassette("TestOffer.get_deal_category"):
            deal_cat = self.moco.DealCategory.getlist()[0]

            return deal_cat

    def get_deal(self):
        user = self.get_user()
        deal_cat = self.get_deal_category()

        with self.recorder.use_cassette("TestOffer.get_deal"):
            deal = self.moco.Deal.create(
                name="TestOffer.get_deal",
                currency="EUR",
                money=1000,
                reminder_date=date(2020, 1, 1),
                user_id=user.id,
                deal_category_id=deal_cat.id
            )

            return deal.data

    def get_customer(self):
        with self.recorder.use_cassette("TestOffer.get_customer"):
            customer = self.moco.Company.getlist(
                company_type="customer"
            )[0]

            return customer

    def get_project(self):
        leader = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestOffer.get_project"):
            project_create = self.moco.Project.create(
                name="TestOffer.get_project",
                currency="EUR",
                leader_id=leader.id,
                customer_id=customer.id,
                finish_date=date(2020, 1, 1),
            )

            return project_create.data

    def get_contact(self):
        with self.recorder.use_cassette("TestOffer.get_contact"):
            contact_create = self.moco.Contact.create(
                firstname="-",
                lastname="TestOffer.get_contact",
                gender=ContactGender.FEMALE
            )

            return contact_create.data

    def test_getlist(self):
        with self.recorder.use_cassette("TestOffer.test_getlist"):
            off_getlist = self.moco.Offer.getlist()

            assert off_getlist.response.status_code == 200

            assert type(off_getlist) is PagedListResponse

            assert off_getlist.current_page == 1
            assert off_getlist.is_last is not None
            assert off_getlist.next_page is not None
            assert off_getlist.total is not None
            assert off_getlist.page_size is not None

    def test_getlist_full(self):
        with self.recorder.use_cassette("TestOffer.test_getlist_full"):
            off_getlist = self.moco.Offer.getlist(
                status=OfferStatus.ACCEPTED,
                from_date=date(2020, 1, 1),
                to_date=date(2020, 1, 31),
                identifier="TEST-IDENT"
            )

            assert off_getlist.response.status_code == 200

            assert type(off_getlist) is PagedListResponse

            assert off_getlist.current_page == 1
            assert off_getlist.is_last is not None
            assert off_getlist.next_page is not None
            assert off_getlist.total is not None
            assert off_getlist.page_size is not None

    def test_get(self):
        deal = self.get_deal()
        user = self.get_user()

        with self.recorder.use_cassette("TestOffer.test_get"):
            rec_address = "My Customer Address 33"
            creation_date = date(2020, 1, 2)
            due_date = date(2021, 1, 1)
            title = "TestOffer.get_get_create"
            tax = 21.5
            currency = "EUR"

            gen = OfferItemGenerator()
            items = [
                gen.generate_title(
                    title="This is the title of the offer"
                ),
                gen.generate_description(
                    description="this is the description"
                ),
                gen.generate_item(
                    title="MailChimp Setup",
                    quantity=1,
                    unit="h",
                    unit_price=100.0,
                    net_total=400
                ),
                gen.generate_item(
                    title="On-Site Support",
                    quantity=20,
                    unit_price=20,
                    unit="h",
                    net_total=400,
                    optional=True
                )
            ]

            offer_create = self.moco.Offer.create(
                deal_id=deal.id,
                project_id=None,
                recipient_address=rec_address,
                creation_date=creation_date,
                due_date=due_date,
                title=title,
                tax=tax,
                currency=currency,
                items=items
            )

            offer_get = self.moco.Offer.get(
                offer_id=offer_create.data.id
            )

            assert offer_create.response.status_code == 201
            assert offer_get.response.status_code == 200

            assert type(offer_create) is ObjectResponse
            assert type(offer_get) is ObjectResponse

            assert offer_get.data.deal.id == deal.id
            assert offer_get.data.date == creation_date.isoformat()
            assert offer_get.data.due_date == due_date.isoformat()
            assert offer_get.data.title == title
            assert offer_get.data.tax == tax
            assert offer_get.data.currency == currency

    def test_create_from_deal(self):
        deal = self.get_deal()

        with self.recorder.use_cassette("TestOffer.test_create_from_deal"):
            rec_address = "My Customer Address 34"
            creation_date = date(2020, 1, 2)
            due_date = date(2021, 1, 1)
            title = "TestOffer.test_create_from_deal"
            tax = 21.5
            currency = "EUR"

            gen = OfferItemGenerator()
            items = [
                gen.generate_title(
                    title="This is the title of the offer"
                ),
                gen.generate_description(
                    description="this is the description"
                ),
                gen.generate_item(
                    title="MailChimp Setup",
                    quantity=1,
                    unit="h",
                    unit_price=100.0,
                    net_total=400
                ),
                gen.generate_item(
                    title="On-Site Support",
                    quantity=20,
                    unit_price=20,
                    unit="h",
                    net_total=400,
                    optional=True
                )
            ]

            offer_create = self.moco.Offer.create(
                deal_id=deal.id,
                project_id=None,
                recipient_address=rec_address,
                creation_date=creation_date,
                due_date=due_date,
                title=title,
                tax=tax,
                currency=currency,
                items=items
            )

            assert offer_create.response.status_code == 201

            assert type(offer_create) is ObjectResponse

            assert offer_create.data.deal.id == deal.id
            assert offer_create.data.date == creation_date.isoformat()
            assert offer_create.data.due_date == due_date.isoformat()
            assert offer_create.data.title == title
            assert offer_create.data.tax == tax
            assert offer_create.data.currency == currency

    def test_create_with_all_items(self):
        deal = self.get_deal()

        with self.recorder.use_cassette("TestOffer.test_create_with_all_items"):
            gen = OfferItemGenerator()
            items = [
                gen.generate_title(
                    title="this is the title"
                ),
                gen.generate_description(
                    description="This is the first description"
                ),
                gen.generate_detail_position(
                    title="support",
                    quantity=1,
                    unit="h",
                    unit_price=65
                ),
                gen.generate_lump_position(
                    title="server hardware",
                    net_total=200
                ),
                gen.generate_subtotal(
                    title="subtotal position"
                ),
                gen.generate_detail_position(
                    title="special support",
                    quantity=3,
                    unit="h",
                    unit_price=90
                ),
                gen.generate_pagebreak()
            ]

            offer_create = self.moco.Offer.create(
                deal_id=deal.id,
                project_id=None,
                recipient_address="My Customer Address 43",
                creation_date=date(2020, 1, 1),
                due_date=date(2021, 1, 1),
                title="TestOffer.test_create_with_all_items",
                tax=19,
                currency="EUR",
                items=items
            )

            assert offer_create.response.status_code == 201

            assert type(offer_create) is ObjectResponse

            assert len(offer_create.data.items) == 7

    def test_create_with_project(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestOffer.test_create_with_project"):
            rec_address = "My Customer Address 34"
            creation_date = date(2020, 1, 2)
            due_date = date(2021, 1, 1)
            title = "TestOffer.test_create_project"
            tax = 21.5
            currency = "EUR"

            gen = OfferItemGenerator()
            items = [
                gen.generate_title(
                    title="offer from project title"
                ),
                gen.generate_lump_position(
                    title="misc",
                    net_total=2000
                )
            ]

            offer_create = self.moco.Offer.create(
                deal_id=None,
                project_id=project.id,
                recipient_address=rec_address,
                creation_date=creation_date,
                due_date=due_date,
                title=title,
                tax=tax,
                currency=currency,
                items=items
            )

            assert offer_create.response.status_code == 201

            assert type(offer_create) is ObjectResponse

            assert offer_create.data.project.id == project.id
            assert offer_create.data.date == creation_date.isoformat()
            assert offer_create.data.title == title
            assert offer_create.data.tax == tax
            assert offer_create.data.currency == currency

    def test_create_with_company(self):
        company = self.get_customer()

        with self.recorder.use_cassette("TestOffer.test_create_with_company"):
            rec_address = "My Customer Address 34"
            creation_date = date(2020, 1, 2)
            due_date = date(2021, 1, 1)
            title = "TestOffer.test_create_company"
            tax = 21.5
            currency = "EUR"

            gen = OfferItemGenerator()
            items = [
                gen.generate_title(
                    title="offer from company title"
                ),
                gen.generate_lump_position(
                    title="misc",
                    net_total=2000
                )
            ]

            offer_create = self.moco.Offer.create(
                deal_id=None,
                company_id=company.id,
                recipient_address=rec_address,
                creation_date=creation_date,
                due_date=due_date,
                title=title,
                tax=tax,
                currency=currency,
                items=items
            )

            assert offer_create.response.status_code == 201

            assert type(offer_create) is ObjectResponse

            assert offer_create.data.company.id == company.id
            assert offer_create.data.date == creation_date.isoformat()
            assert offer_create.data.title == title
            assert offer_create.data.tax == tax
            assert offer_create.data.currency == currency

    def test_create_full(self):
        project = self.get_project()
        contact = self.get_contact()
        deal = self.get_deal()

        with self.recorder.use_cassette("TestOffer.test_create_full"):
            rec_address = "My Customer Address 34"
            creation_date = date(2020, 1, 2)
            due_date = date(2021, 1, 1)
            title = "TestOffer.test_create_full"
            tax = 21.5
            currency = "EUR"
            salutation = "salute"
            footer = "footer"
            discount = 20

            gen = OfferItemGenerator()
            items = [
                gen.generate_title(
                    title="offer from project title"
                ),
                gen.generate_lump_position(
                    title="misc",
                    net_total=2000
                )
            ]

            offer_create = self.moco.Offer.create(
                deal_id=deal.id,
                project_id=project.id,
                recipient_address=rec_address,
                creation_date=creation_date,
                due_date=due_date,
                title=title,
                tax=tax,
                currency=currency,
                items=items,
                salutation=salutation,
                footer=footer,
                discount=discount,
                contact_id=contact.id
            )

            assert offer_create.response.status_code == 201

            assert type(offer_create) is ObjectResponse

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
                gen.generate_title(
                    title="title"
                ),
                gen.generate_lump_position(
                    title="pos 1",
                    net_total=200
                )
            ]

            offer_create = self.moco.Offer.create(
                deal_id=None,
                project_id=project.id,
                recipient_address="My Customer Address 24",
                creation_date=date(2020, 1, 1),
                due_date=date(2021, 1, 1),
                title="TestOffer.test_pdf_create",
                tax=21,
                currency="EUR",
                items=items
            )

            offer_pdf = self.moco.Offer.pdf(
                offer_id=offer_create.data.id
            )

            assert offer_create.response.status_code == 201
            assert offer_pdf.response.status_code == 200

            assert type(offer_pdf) is FileResponse

    def test_update_status(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestOffer.test_update_status"):
            offer_status = OfferStatus.ACCEPTED

            gen = OfferItemGenerator()
            items = [
                gen.generate_title(
                    title="title"
                ),
                gen.generate_lump_position(
                    title="pos 1",
                    net_total=200
                )
            ]

            offer_create = self.moco.Offer.create(
                deal_id=None,
                project_id=project.id,
                recipient_address="My Customer Address 44",
                creation_date=date(2020, 1, 1),
                due_date=date(2021, 1, 1),
                title="TestOffer.test_update_status_create",
                tax=21,
                currency="EUR",
                items=items
            )

            offer_update_status = self.moco.Offer.update_status(
                offer_id=offer_create.data.id,
                status=offer_status
            )

            offer_get = self.moco.Offer.get(
                offer_id=offer_create.data.id
            )

            assert offer_create.response.status_code == 201
            assert offer_update_status.response.status_code == 204
            assert offer_get.response.status_code == 200

            assert type(offer_create) is ObjectResponse
            assert type(offer_update_status) is EmptyResponse
            assert type(offer_get) is ObjectResponse

            assert offer_create.data.status == OfferStatus.CREATED
            assert offer_get.data.status == offer_status
