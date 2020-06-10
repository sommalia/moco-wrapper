import datetime

from .. import IntegrationTest
from moco_wrapper.models.purchase import PurchasePaymentMethod
from moco_wrapper.util.generator import PurchaseItemGenerator
from moco_wrapper.util.response import JsonResponse, ListingResponse
from moco_wrapper.models.company import CompanyType

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

            assert isinstance(purchase_create, JsonResponse)
            
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
                "test" : "vars"
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

            assert isinstance(purchase_create, JsonResponse)

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


        