from .. import IntegrationTest

from datetime import date

from moco_wrapper.util.response import JsonResponse, ListingResponse
from moco_wrapper.models.invoice import InvoiceStatus, InvoiceChangeAddress

class TestInvoice(IntegrationTest):
    def test_getlist(self):
        with self.recorder.use_cassette("TestInvoice.test_getlist"):
            inv_getlist = self.moco.Invoice.getlist()

            assert inv_getlist.response.status_code == 200

            assert isinstance(inv_getlist, ListingResponse)

    def test_locked(self):
        with self.recorder.use_cassette("TestInvoice.test_locked"):
            inv_locked = self.moco.Invoice.locked()

            assert inv_locked.response.status_code == 200
            
            assert isinstance(inv_locked, ListingResponse)

    def test_get(self):
        #create minimal invoice
        pass

    def test_pdf(self):
        #create minimal invoice
        pass

    def test_timesheet(self):
        #create minimal invoice
        pass

    def test_update_status(self):
        #create minimal invoice
        pass

    def test_create(self):
        pass
        
