from moco_wrapper.util.generator import InvoicePaymentGenerator
from .. import UnitTest
import pytest



class TestInvoicePayment(UnitTest):
    def test_getlist(self):
        response = self.moco.InvoicePayment.getlist()

        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        sort_by = "test field to sort by"

        response = self.moco.InvoicePayment.getlist(sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "test field to sort by"
        sort_order = "desc"

        response = self.moco.InvoicePayment.getlist(sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        page_default = 1

        response = self.moco.InvoicePayment.getlist()
        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.InvoicePayment.getlist(page=page_overwrite)
        assert response["params"]["page"] == page_overwrite

    def test_get(self):
        payment_id = 5

        response = self.moco.InvoicePayment.get(payment_id)

        assert response["method"] == "GET"

    def test_create(self):
        invoice_id = 3
        date = '2020-05-05'
        paid_total = 200
        currency = "EUR"

        response = self.moco.InvoicePayment.create(date, invoice_id, paid_total, currency)
        data = response["data"]

        assert data["invoice_id"] == invoice_id
        assert data["date"] == date
        assert data["paid_total"] == paid_total
        assert data["currency"] == currency

        assert response["method"] == "POST"
    
    def test_create_bulk(self):
        generator = InvoicePaymentGenerator()

        items = [generator.generate('2019-10-10', 1, 200, "EUR"), generator.generate('2020-05-05', 2, 420, "CHF")]  
        response = self.moco.InvoicePayment.create_bulk(items)

        assert response["data"]["bulk_data"] == items
        assert response["method"] == "POST"


    def test_update(self):
        payment_id = 54
        date = '2020-05-05'
        paid_total = 200
        currency = "EUR"

        response = self.moco.InvoicePayment.update(payment_id, date=date, paid_total=paid_total, currency=currency)
        data = response["data"]

        assert data["date"] == date
        assert data["paid_total"] == paid_total
        assert data["currency"] == currency

        assert response["method"] == "PUT"

    def test_delete(self):
        payment_id = 123

        response = self.moco.InvoicePayment.delete(payment_id)

        assert response["method"] == "DELETE"

