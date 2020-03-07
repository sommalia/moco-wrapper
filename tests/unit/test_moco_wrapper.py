import pytest

from . import UnitTest

from moco_wrapper import moco, util, models

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
        assert isinstance(self.moco.UserPresence, models.UserPresence)

    def test_holiday_set(self):
        assert isinstance(self.moco.UserHoliday, models.UserHoliday)

    def test_employment_set(self):
        assert isinstance(self.moco.UserEmployment, models.UserEmployment)

    def test_project_recurring_expense_set(self):
        assert isinstance(self.moco.ProjectRecurringExpense, models.ProjectRecurringExpense)

    def test_session_set(self):
        assert isinstance(self.moco.Session, models.Session)

    def test_project_payment_schedule_set(self):
        assert isinstance(self.moco.ProjectPaymentSchedule, models.ProjectPaymentSchedule)

    def test_wrapper_init(self):
        new_moco = moco.Moco(
            auth={
                "api_key" : "api_key",
                "domain" : "domain"
            }
        )
        new_moco.authenticate()

        assert new_moco.api_key == "api_key"
        assert new_moco.domain == "domain"

        assert isinstance(new_moco._requestor, util.requestor.DefaultRequestor)

    def test_wrapper_init_requestor_overwrite(self):
        new_moco = moco.Moco(
            auth={
                "api_key" : "api_key",
                "domain" : "domain"
            },
            requestor=util.requestor.RawRequestor()
        )

        new_moco.authenticate()
        
        assert new_moco.api_key == "api_key"
        assert new_moco.domain == "domain"

        assert isinstance(new_moco._requestor, util.requestor.RawRequestor)

    def test_wrapper_init_impersonation(self):
        impersonate_user_id = 123
        new_moco = moco.Moco(impersonate_user_id=impersonate_user_id)

        assert new_moco._impersonation_user_id == impersonate_user_id

    def test_wrapper_impersonate(self):
        impersonate_user_id = 123
        new_moco = moco.Moco()
        new_moco.impersonate(impersonate_user_id)

        assert new_moco._impersonation_user_id == impersonate_user_id

    def test_wrapper_clear_impersonation(self):
        impersonate_user_id = 123
        new_moco = moco.Moco()
        new_moco.impersonate(impersonate_user_id)

        assert new_moco._impersonation_user_id == impersonate_user_id

        new_moco.clear_impersonation()
        
        assert new_moco._impersonation_user_id is None