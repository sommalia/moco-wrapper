import pytest
import datetime
from .. import UnitTest

from moco_wrapper.models.purchase import PurchasePaymentMethod
from moco_wrapper.util.generator import PurchaseItemGenerator


class TestPurchase(UnitTest):
    def test_getlist_sort_default(self):
        sort_by = "field to sort by"

        response = self.moco.Purchase.getlist(
            sort_by=sort_by
        )

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "field to sort by"
        sort_order = "desc"

        response = self.moco.Purchase.getlist(
            sort_by=sort_by,
            sort_order=sort_order
        )

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        page_default = 1

        response = self.moco.Purchase.getlist()

        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.Purchase.getlist(
            page=page_overwrite
        )

        assert response["params"]["page"] == page_overwrite

    def test_getlist_throws_only_start_date(self):
        with pytest.raises(ValueError):
            self.moco.Purchase.getlist(
                start_date='2020-02-10',
                end_date=None
            )

    def test_getlist_throws_only_end_date(self):
        with pytest.raises(ValueError):
            self.moco.Purchase.getlist(
                start_date=None,
                end_date='2020-10-10'
            )

    def test_getlist(self):
        purchase_id = 123
        category_id = 456
        term = "this is the term"
        company_id = 444
        status = "pending"
        tags = ["these", "are", "tags"]
        start_date = "2020-01-04"
        end_date = "2020-04-04"
        unpaid = True
        payment_method = PurchasePaymentMethod.PAYPAL

        response = self.moco.Purchase.getlist(
            purchase_id=purchase_id,
            category_id=category_id,
            term=term,
            company_id=company_id,
            status=status,
            tags=tags,
            start_date=start_date,
            end_date=end_date,
            unpaid=unpaid,
            payment_method=payment_method
        )

        params = response["params"]

        assert response["method"] == "GET"

        assert params["id"] == purchase_id
        assert params["category_id"] == category_id
        assert params["term"] == term
        assert params["company_id"] == company_id
        assert params["status"] == status
        assert sorted(params["tags"]) == sorted(tags)
        assert params["date"] == "{}:{}".format(start_date, end_date)
        assert params["unpaid"] == unpaid
        assert params["payment_method"] == payment_method

    def test_create(self):
        generator = PurchaseItemGenerator()

        purchase_date = "2020-04-01"
        currency = "EUR"
        payment_method = "PAYPAL"
        items = [
            generator.generate_item(
                title="title",
                total=100,
                tax=7.4
            )
        ]

        due_date = "2020-04-30"
        service_from = datetime.date(2020, 5, 1)
        service_to = datetime.date(2020, 5, 31)
        company_id = 34
        receipt_identifier = "REC-1"
        info = "infotext"
        iban = "DE1234"
        reference = "REF-2"
        custom_properties = {
            "this": "custom"
        }
        file = {
            "filename": "this is the filename",
            "base64": "base64 encoded values"
        }
        tags = ["these", "are", "tags"]

        response = self.moco.Purchase.create(
            purchase_date=purchase_date,
            currency=currency,
            payment_method=payment_method,
            items=items,
            due_date=due_date,
            service_period_from=service_from,
            service_period_to=service_to,
            company_id=company_id,
            receipt_identifier=receipt_identifier,
            info=info,
            iban=iban,
            reference=reference,
            custom_properties=custom_properties,
            file=file,
            tags=tags
        )

        data = response["data"]

        assert response["method"] == "POST"

        assert data["date"] == purchase_date
        assert data["currency"] == currency
        assert data["payment_method"] == payment_method
        assert data["items"] == items
        assert data["due_date"] == due_date
        assert data["service_period_from"] == service_from.isoformat()
        assert data["service_period_to"] == service_to.isoformat()
        assert data["company_id"] == company_id
        assert data["info"] == info
        assert data["iban"] == iban
        assert data["reference"] == reference
        assert data["custom_properties"] == custom_properties
        assert data["file"] == file
        assert data["tags"] == tags

    def test_get(self):
        purchase_id = 212

        response = self.moco.Purchase.get(
            purchase_id=purchase_id
        )

        assert response["method"] == "GET"

    def test_delete(self):
        purchase_id = 212

        response = self.moco.Purchase.delete(
            purchase_id=purchase_id
        )

        assert response["method"] == "DELETE"

    def test_update_status(self):
        purchase_id = 234
        status = "approved"

        response = self.moco.Purchase.update_status(
            purchase_id=purchase_id,
            status=status
        )

        print(response)
        data = response["data"]

        assert response["method"] == "PATCH"

        assert data["status"] == status
