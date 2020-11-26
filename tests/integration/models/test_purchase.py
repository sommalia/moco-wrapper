import datetime

from .. import IntegrationTest
from moco_wrapper.models.purchase import PurchasePaymentMethod, PurchaseFile, PurchaseStatus
from moco_wrapper.util.generator import PurchaseItemGenerator
from moco_wrapper.util.response import ObjectResponse, PagedListResponse, EmptyResponse
from moco_wrapper.models.company import CompanyType
from os import path


class TestPurchase(IntegrationTest):
    def get_company(self):
        with self.recorder.use_cassette("TestPurchase.get_company"):
            company_create = self.moco.Company.create(
                "dummy supplier, test purchase",
                CompanyType.SUPPLIER
            )
            return company_create.data

    def test_create(self):
        with self.recorder.use_cassette("TestPurchase.test_create"):
            generator = PurchaseItemGenerator()

            currency = "EUR"
            payment_method = PurchasePaymentMethod.PAYPAL
            purchase_date = datetime.date(2020, 4, 1)

            item_title = "dummy purchase item title"

            items = [
                generator.generate_item(item_title, 200.2, 4.3)
            ]

            purchase_create = self.moco.Purchase.create(
                purchase_date,
                currency,
                payment_method,
                items,
            )

            assert purchase_create.response.status_code == 200

            assert type(purchase_create) is ObjectResponse

            assert purchase_create.data.payment_method == payment_method
            assert purchase_create.data.currency == currency
            assert len(purchase_create.data.items) == 1
            assert purchase_create.data.date == purchase_date.isoformat()

    def test_create_full(self):
        supplier = self.get_company()

        with self.recorder.use_cassette("TestPurchase.test_create_full"):
            generator = PurchaseItemGenerator()

            purchase_date = datetime.date(2020, 1, 1)
            currency = "EUR"
            payment_method = "bank_transfer"
            items = [
                generator.generate_item("dummy purchase item, first", 100, 2, tax_included=False),
                generator.generate_item("dummy purchase item, second", 200, 3.5)
            ]

            due_date = datetime.date(2021, 1, 1)
            service_period_from = datetime.date(2020, 1, 1)
            service_period_to = datetime.date(2020, 12, 31)
            company_id = supplier.id
            receipt_identifier = self.id_generator()
            info = "dummy info text"
            reference = "reference text"
            custom_properties = {
                "test": "vars"
            }

            tags = ["dummy file"]

            purchase_create = self.moco.Purchase.create(
                purchase_date,
                currency,
                payment_method,
                items,
                due_date=due_date,
                service_period_from=service_period_from,
                service_period_to=service_period_to,
                company_id=company_id,
                receipt_identifier=receipt_identifier,
                info=info,
                reference=reference,
                custom_properties=custom_properties,
                tags=tags
            )

            assert purchase_create.response.status_code == 200

            assert type(purchase_create) is ObjectResponse

            assert purchase_create.data.date == purchase_date.isoformat()
            assert purchase_create.data.currency == currency
            assert purchase_create.data.payment_method == payment_method
            assert len(purchase_create.data.items) == 2
            assert purchase_create.data.due_date == due_date.isoformat()
            assert purchase_create.data.service_period_from == service_period_from.isoformat()
            assert purchase_create.data.service_period_to == service_period_to.isoformat()
            assert purchase_create.data.company.id == company_id
            assert purchase_create.data.custom_properties is not None
            assert sorted(purchase_create.data.tags) == sorted(tags)
            assert purchase_create.data.user.id is not None

    def test_create_with_file(self):
        pdf_path = path.join(path.dirname(path.dirname(__file__)), "files", "test_purchase_create_with_file.pdf")
        purchase_file = PurchaseFile.load(pdf_path)

        generator = PurchaseItemGenerator()

        with self.recorder.use_cassette("TestPurchase.test_create_with_file"):
            payment_method = PurchasePaymentMethod.CASH
            purchase_date = datetime.date(2020, 1, 1)
            currency = "EUR"
            items = [
                generator.generate_item("dummy items, test create with file", 100.2, 5)
            ]

            purchase_create = self.moco.Purchase.create(
                purchase_date,
                currency,
                payment_method,
                items,
                file=purchase_file
            )

            assert purchase_create.response.status_code == 200

            assert type(purchase_create) is ObjectResponse

            assert purchase_create.data.date == purchase_date.isoformat()
            assert purchase_create.data.currency == currency
            assert purchase_create.data.payment_method == payment_method
            assert len(purchase_create.data.items) == 1

            assert purchase_create.data.file_url is not None

    def test_get(self):
        generator = PurchaseItemGenerator()

        with self.recorder.use_cassette("TestPurchase.test_get"):
            purchase_date = datetime.date(2020, 1, 1)
            currency = "EUR"
            payment_method = PurchasePaymentMethod.DIRECT_DEBIT
            items = [
                generator.generate_item("dummy purchase, test get", 200, 10.5)
            ]

            purchase_create = self.moco.Purchase.create(
                purchase_date,
                currency,
                payment_method,
                items
            )

            purchase_get = self.moco.Purchase.get(
                purchase_create.data.id
            )

            assert purchase_create.response.status_code == 200
            assert purchase_get.response.status_code == 200

            assert type(purchase_create) is ObjectResponse
            assert type(purchase_get) is ObjectResponse

            assert purchase_get.data.date == purchase_date.isoformat()
            assert purchase_get.data.currency == currency
            assert purchase_get.data.payment_method == payment_method
            assert len(purchase_get.data.items) == 1

    def test_delete(self):
        generator = PurchaseItemGenerator()

        with self.recorder.use_cassette("TestPurchase.test_delete"):
            purchase_create = self.moco.Purchase.create(
                datetime.date(2020, 1, 2),
                "EUR",
                PurchasePaymentMethod.CASH,
                [
                    generator.generate_item("dummy item, test delete", 20, 1)
                ]
            )

            purchase_delete = self.moco.Purchase.delete(purchase_create.data.id)

            assert purchase_create.response.status_code == 200
            assert purchase_delete.response.status_code == 200

            assert type(purchase_create) is ObjectResponse
            assert type(purchase_delete) is EmptyResponse

    def test_update_status(self):
        generator = PurchaseItemGenerator()

        with self.recorder.use_cassette("TestPurchase.test_update_status"):
            purchase_create = self.moco.Purchase.create(
                datetime.date(2020, 2, 4),
                "EUR",
                PurchasePaymentMethod.PAYPAL,
                [
                    generator.generate_item("dummy purchase, test update status", 100, 2)
                ]
            )

            purchase_update_status = self.moco.Purchase.update_status(
                purchase_create.data.id,
                PurchaseStatus.APPROVED
            )

            purchase_get = self.moco.Purchase.get(
                purchase_create.data.id
            )

            assert purchase_create.response.status_code == 200
            assert purchase_update_status.response.status_code == 200
            assert purchase_get.response.status_code == 200

            assert type(purchase_create) is ObjectResponse
            assert type(purchase_update_status) is EmptyResponse
            assert type(purchase_get) is ObjectResponse

            assert purchase_create.data.status == PurchaseStatus.PENDING
            assert purchase_get.data.status == PurchaseStatus.APPROVED

    def test_store_document(self):
        pdf_path = path.join(path.dirname(path.dirname(__file__)), "files", "test_purchase_store_document.pdf")
        purchase_file = PurchaseFile.load(pdf_path)

        generator = PurchaseItemGenerator()

        with self.recorder.use_cassette("TestPurchase.test_store_document"):
            purchase_create = self.moco.Purchase.create(
                datetime.date(2020, 2, 4),
                "EUR",
                PurchasePaymentMethod.PAYPAL,
                [
                    generator.generate_item("dummy purchase, test update status", 100, 2)
                ]
            )

            purchase_store_doc = self.moco.Purchase.store_document(purchase_create.data.id, purchase_file)

            purchase_get = self.moco.Purchase.get(
                purchase_create.data.id
            )

            assert purchase_create.response.status_code == 200
            assert purchase_store_doc.response.status_code == 200
            assert purchase_get.response.status_code == 200

            assert type(purchase_create) is ObjectResponse
            assert type(purchase_store_doc) is EmptyResponse
            assert type(purchase_get) is ObjectResponse

            assert purchase_create.data.file_url is None
            assert purchase_get.data.file_url is not None

    def test_getlist_full(self):
        with self.recorder.use_cassette("TestPurchase.test_getlist"):
            purchase_list = self.moco.Purchase.getlist()

            assert purchase_list.response.status_code == 200

            assert type(purchase_list) is PagedListResponse

