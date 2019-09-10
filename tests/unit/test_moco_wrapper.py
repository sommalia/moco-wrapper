import pytest

from . import UnitTest
from moco_wrapper import models
from moco_wrapper import util
from moco_wrapper import moco_wrapper

class TestMocoWrapper(UnitTest):

    def test_activity_set(self):
        assert isinstance(self.moco.Activity, models.Activity)

    def test_contact_set(self):
        assert isinstance(self.moco.Contact, models.Contact)

    def test_company_set(self):
        assert isinstance(self.moco.Company, models.Company)

    def test_comment_set(self):
        assert isinstance(self.moco.Comment, models.Comment)

    def test_unit_set(self):
        assert isinstance(self.moco.Unit, models.Unit)

    def test_user_set(self):
        assert isinstance(self.moco.User, models.User)

    def test_schedule_set(self):
        assert isinstance(self.moco.Schedule, models.Schedule)

    def test_project_set(self):
        assert isinstance(self.moco.Project, models.Project)

    def test_project_expense_set(self):
        assert isinstance(self.moco.ProjectExpense, models.ProjectExpense)

    def test_contact_set(self):
        assert isinstance(self.moco.ProjectContract, models.ProjectContract)

    def test_project_task_set(self):
        assert isinstance(self.moco.ProjectTask, models.ProjectTask)

    def test_deal_set(self):
        assert isinstance(self.moco.Deal, models.Deal)

    def test_invoice_set(self):
        assert isinstance(self.moco.Invoice, models.Invoice)

    def test_invoice_payment_set(self):
        assert isinstance(self.moco.InvoicePayment, models.InvoicePayment)

    def test_offer_set(self):
        assert isinstance(self.moco.Offer, models.Offer)

    def test_presence_set(self):
        assert isinstance(self.moco.Presence, models.Presence)

    def test_holiday_set(self):
        assert isinstance(self.moco.Holiday, models.Holiday)

    def test_employment_set(self):
        assert isinstance(self.moco.Employment, models.Employment)

    def test_project_recurring_expense_set(self):
        assert isinstance(self.moco.ProjectRecurringExpense, models.ProjectRecurringExpense)

    def test_wrapper_init(self):
        new_moco = moco_wrapper.Moco(api_key="api_key", domain="domain")
        assert new_moco.api_key == "api_key"
        assert new_moco.domain == "domain"

        assert isinstance(new_moco._requestor, util.RateLimitedRequestor)

    def test_wrapper_init_requestor_overwrite(self):
        new_moco = moco_wrapper.Moco(api_key="api_key", domain="domain", http=util.TestRequester())
        assert new_moco.api_key == "api_key"
        assert new_moco.domain == "domain"

        assert isinstance(new_moco._requestor, util.TestRequester)