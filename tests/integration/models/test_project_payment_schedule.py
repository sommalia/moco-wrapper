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
        project = self.get_project()
        
        with self.recorder.use_cassette("TestProjectPaymentSchedule.test_getlist"):
            sched_list = self.moco.ProjectPaymentSchedule.getlist(project.id, sort_by="net_total")

            assert sched_list.response.status_code == 200

            assert isinstance(sched_list, ListingResponse)

    def test_get(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectPaymentSchedule.test_get"):
            net_total = 100
            sched_date = date(2020, 1, 1)
            title = "dummy project expense, test get"
            checked = True

            sched_create = self.moco.ProjectPaymentSchedule.create(
                project.id,
                net_total,
                sched_date,
                title=title,
                checked=checked
            )

            sched_get = self.moco.ProjectPaymentSchedule.get(
                project.id,
                sched_create.data.id
            )

            assert sched_create.response.status_code == 200
            assert sched_get.response.status_code == 200

            assert isinstance(sched_create, JsonResponse)
            assert isinstance(sched_get, JsonResponse)

            assert sched_get.data.date == sched_date.isoformat()
            assert sched_get.data.net_total == net_total
            assert sched_get.data.project.id == project.id
            assert sched_get.data.title == title
            assert sched_get.data.checked == checked


    def test_create(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectPaymentSchedule.test_create"):
            net_total = 100
            sched_date = date(2020, 1, 1)

            sched_create = self.moco.ProjectPaymentSchedule.create(
                project.id,
                net_total,
                sched_date
            )

            assert sched_create.response.status_code == 200
            
            assert isinstance(sched_create, JsonResponse)

            assert sched_create.data.date == sched_date.isoformat()
            assert sched_create.data.net_total == net_total
            assert sched_create.data.project.id == project.id

    def test_create_full(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectPaymentSchedule.test_create_full"):
            net_total = 100
            sched_date = date(2020, 1, 1)
            title = "dummy project expense, test create full"
            checked = True

            sched_create = self.moco.ProjectPaymentSchedule.create(
                project.id,
                net_total,
                sched_date,
                title=title,
                checked=checked
            )

            assert sched_create.response.status_code == 200
            
            assert isinstance(sched_create, JsonResponse)

            assert sched_create.data.date == sched_date.isoformat()
            assert sched_create.data.net_total == net_total
            assert sched_create.data.project.id == project.id
            assert sched_create.data.title == title
            assert sched_create.data.checked == checked

    def test_update(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectPaymentSchedule.test_update"):
            net_total = 100
            sched_date = date(2020, 3, 1)
            title = "dummy project expense, test update"
            checked = True

            sched_create = self.moco.ProjectPaymentSchedule.create(
                project.id,
                1,
                date(2020, 12, 1)
            )

            sched_update = self.moco.ProjectPaymentSchedule.update(
                project.id,
                sched_create.data.id,
                net_total=net_total,
                schedule_date=sched_date,
                title=title,
                checked=checked
            )

            assert sched_create.response.status_code == 200
            assert sched_update.response.status_code == 200

            assert isinstance(sched_create, JsonResponse)
            assert isinstance(sched_update, JsonResponse)

            assert sched_update.data.date == sched_date.isoformat()
            assert sched_update.data.net_total == net_total
            assert sched_update.data.project.id == project.id
            assert sched_update.data.title == title
            assert sched_update.data.checked == checked


    def test_delete(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestProjectPaymentSchedule.test_delete"):
            sched_create = self.moco.ProjectPaymentSchedule.create(
                project.id,
                1,
                date(2020, 12, 1)
            )

            sched_delete = self.moco.ProjectPaymentSchedule.delete(
                project.id, 
                sched_create.data.id
            )

            assert sched_create.response.status_code == 200
            assert sched_delete.response.status_code == 200

            assert isinstance(sched_create, JsonResponse)
            assert isinstance(sched_delete, JsonResponse)
