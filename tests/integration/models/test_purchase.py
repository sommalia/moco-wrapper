import datetime

from .. import IntegrationTest
from moco_wrapper.models.purchase import PurchasePaymentMethod
from moco_wrapper.util.generator import PurchaseItemGenerator
from moco_wrapper.util.response import JsonResponse, ListingResponse

class TestPurchase(IntegrationTest):

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