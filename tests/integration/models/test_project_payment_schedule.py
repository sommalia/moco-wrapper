from .. import IntegrationTest
from datetime import date

from moco_wrapper.util.response import JsonResponse, ListingResponse, EmptyResponse

class TestProjectPaymentSchedule(IntegrationTest):
    def get_customer(self):
        with self.recorder.use_cassette("TestProjectPaymentSchedule.get_customer"):
            customer_create = self.moco.Company.create(
                "dummy customer, test project payment scheduke",
                "customer"
            )

            return customer_create.data
    
    def get_user(self):
        with self.recorder.use_cassette("TestProjectPaymentSchedule.get_user"):
            user = self.moco.User.getlist().items[0]
            return user
    
    def get_project(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProjectPaymentSchedule.get_project"):
            project_create = self.moco.Project.create(
                "dummy project, test payment schedule",
                "EUR",
                user.id,
                customer.id,
                fixed_price=True,
                budget=1000.0
            )

            return project_create.data
    
    def test_getlist(self):
        pass

    def test_get(self):
        pass

    def test_create(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectPaymentSchedule.test_create"):
            net_total = 100
            sched_date = date(2020, 1, 1)

            schedule_create = self.moco.ProjectPaymentSchedule.create(
                project.id,
                net_total,
                sched_date
            )

            assert schedule_create.response.status_code == 200
            
            assert isinstance(schedule_create, JsonResponse)

            assert schedule_create.data.date == sched_date.isoformat()
            assert schedule_create.data.net_total == net_total
            assert schedule_create.data.project.id == project.id

    def test_create_full(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass