from moco_wrapper import models as m
from moco_wrapper.util.endpoint import Endpoint


class EndpointManager(object):
    """
    Class for managing all models that the moco class uses
    """
    def __init__(self):
        """
        Class constructor
        """
        self.map = {}

        self.endpoints = []

        self.endpoints.extend(m.AccountFixedCost.endpoints())
        self.endpoints.extend(m.Activity.endpoints())
        self.endpoints.extend(m.Comment.endpoints())
        self.endpoints.extend(m.Company.endpoints())
        self.endpoints.extend(m.Contact.endpoints())
        self.endpoints.extend(m.Deal.endpoints())
        self.endpoints.extend(m.DealCategory.endpoints())
        self.endpoints.extend(m.AccountHourlyRate.endpoints())
        self.endpoints.extend(m.Invoice.endpoints())
        self.endpoints.extend(m.InvoicePayment.endpoints())
        self.endpoints.extend(m.Offer.endpoints())
        self.endpoints.extend(m.PlanningEntry.endpoints())
        self.endpoints.extend(m.Project.endpoints())
        self.endpoints.extend(m.ProjectContract.endpoints())
        self.endpoints.extend(m.ProjectExpense.endpoints())
        self.endpoints.extend(m.ProjectPaymentSchedule.endpoints())
        self.endpoints.extend(m.ProjectRecurringExpense.endpoints())
        self.endpoints.extend(m.ProjectTask.endpoints())
        self.endpoints.extend(m.Purchase.endpoints())
        self.endpoints.extend(m.PurchaseCategory.endpoints())
        self.endpoints.extend(m.PurchaseDraft.endpoints())
        self.endpoints.extend(m.Schedule.endpoints())
        self.endpoints.extend(m.Session.endpoints())
        self.endpoints.extend(m.Tagging.endpoints())
        self.endpoints.extend(m.Unit.endpoints())
        self.endpoints.extend(m.User.endpoints())
        self.endpoints.extend(m.UserEmployment.endpoints())
        self.endpoints.extend(m.UserHoliday.endpoints())
        self.endpoints.extend(m.UserPresence.endpoints())
        self.endpoints.extend(m.AccountInternalHourlyRate.endpoints())
        self.endpoints.extend(m.Report.endpoints())

        self._build_map()

    def _build_map(self):
        for endpoint in self.endpoints:
            self.map[endpoint.slug] = endpoint

    def get(self, slug) -> Endpoint:
        """
        Retrieve an endpoint by its unique slug

        :param slug: Endpoint slug

        :type slug: str

        :return: Endpoint with the given slug, or None if the endpoint does not exist
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`
        """
        return self.map.get(slug, None)
