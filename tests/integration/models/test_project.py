from moco_wrapper.util.response import JsonResponse, ListingResponse
from moco_wrapper.models.project import ProjectBillingVariant

from datetime import date

from .. import IntegrationTest

class TestProject(IntegrationTest):
    def get_unit(self):
        with self.recorder.use_cassette("TestProject.get_unit"):
            unit = self.moco.Unit.getlist().items[0]
            return unit

    def get_user(self):
        with self.recorder.use_cassette("TestProject.get_user"):
            user = self.moco.User.getlist().items[0]
            return user

    def get_other_user(self):
        unit = self.get_unit()

        with self.recorder.use_cassette("TestProject.get_other_user"):
            user_create = self.moco.User.create(
                "dummy user",
                "testing contracts",
                "{}@mycompany.com".format(self.id_generator()),
                self.id_generator(),
                unit.id,
            )

            return user_create.data
    
    def get_customer(self):
        with self.recorder.use_cassette("TestProject.get_customer"):
            customer_create = self.moco.Company.create(
                "TestProject",
                company_type="customer"
            )

            return customer_create.data


    def test_create(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_create"):
            name = "test project create"
            currency = "EUR"
            finish_date = date(2021, 1, 1)
            
            project_create = self.moco.Project.create(
                name,
                currency,
                user.id,
                customer.id,
                finish_date=finish_date
            )

            assert project_create.response.status_code == 200

            assert isinstance(project_create, JsonResponse)

            assert project_create.data.name == name
            assert project_create.data.currency == currency
            assert project_create.data.finish_date == finish_date.isoformat()
            assert project_create.data.leader.id == user.id
            assert project_create.data.customer.id == customer.id

    def test_create_full(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_create_full"):
            name = "test project create"
            currency = "EUR"
            finish_date = date(2021, 1, 1)
            billing_address = "general street 22"
            billing_variant = ProjectBillingVariant.PROJECT
            hourly_rate = 12.5
            budget = 100
            labels = ["low risk", "low income"]
            info = "general information"
            
            project_create = self.moco.Project.create(
                name,
                currency,
                user.id,
                customer.id,
                finish_date=finish_date,
                billing_address=billing_address,
                billing_variant=billing_variant,
                hourly_rate=hourly_rate,
                budget=budget,
                labels=labels,
                info=info
            )

            assert project_create.response.status_code == 200

            assert isinstance(project_create, JsonResponse)

            assert project_create.data.name == name
            assert project_create.data.currency == currency
            assert project_create.data.finish_date == finish_date.isoformat()
            assert project_create.data.leader.id == user.id
            assert project_create.data.customer.id == customer.id
            assert project_create.data.billing_address == billing_address
            assert project_create.data.billing_variant == billing_variant
            assert project_create.data.hourly_rate == hourly_rate
            assert project_create.data.budget == budget
            assert sorted(project_create.data.labels) == sorted(labels)
            assert project_create.data.info == info

    def test_get(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_get"):
            name = "test project get"
            currency = "EUR"
            finish_date = date(2021, 1, 1)
            billing_address = "general street 22"
            billing_variant = ProjectBillingVariant.PROJECT
            hourly_rate = 12.5
            budget = 100
            labels = ["low risk", "low income"]
            info = "general information"
            
            project_create = self.moco.Project.create(
                name,
                currency,
                user.id,
                customer.id,
                finish_date=finish_date,
                billing_address=billing_address,
                billing_variant=billing_variant,
                hourly_rate=hourly_rate,
                budget=budget,
                labels=labels,
                info=info
            )

            project_get = self.moco.Project.get(project_create.data.id)

            assert project_create.response.status_code == 200
            assert project_get.response.status_code == 200

            assert isinstance(project_create, JsonResponse)
            assert isinstance(project_get, JsonResponse)

            assert project_get.data.name == name
            assert project_get.data.currency == currency
            assert project_get.data.finish_date == finish_date.isoformat()
            assert project_get.data.leader.id == user.id
            assert project_get.data.customer.id == customer.id
            assert project_get.data.billing_address == billing_address
            assert project_get.data.billing_variant == billing_variant
            assert project_get.data.hourly_rate == hourly_rate
            assert project_get.data.budget == budget
            assert sorted(project_get.data.labels) == sorted(labels)
            assert project_get.data.info == info

    def test_update(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_update"):
            name = "test project update"
            currency = "EUR"
            finish_date = date(2021, 1, 1)
            billing_address = "general street 22"
            billing_variant = ProjectBillingVariant.PROJECT
            hourly_rate = 12.5
            budget = 100
            labels = ["low risk", "low income"]
            info = "general information"

            project_create = self.moco.Project.create(
                "dummy project, test update",
                "EUR",
                user.id,
                customer.id,
                finish_date = date(2020, 1, 1),
            )
            
            project_update = self.moco.Project.update(
                project_create.data.id,
                name=name,
                finish_date=finish_date,
                leader_id=user.id,
                customer_id=customer.id,
                billing_address=billing_address,
                billing_variant=billing_variant,
                hourly_rate=hourly_rate,
                budget=budget,
                labels=labels,
                info=info
            )

            assert project_create.response.status_code == 200
            assert project_update.response.status_code == 200

            assert isinstance(project_create, JsonResponse)
            assert isinstance(project_update, JsonResponse)

            assert project_update.data.name == name
            assert project_update.data.currency == currency
            assert project_update.data.finish_date == finish_date.isoformat()
            assert project_update.data.leader.id == user.id
            assert project_update.data.customer.id == customer.id
            assert project_update.data.billing_address == billing_address
            assert project_update.data.billing_variant == billing_variant
            assert project_update.data.hourly_rate == hourly_rate
            assert project_update.data.budget == budget
            assert sorted(project_update.data.labels) == sorted(labels)
            assert project_update.data.info == info

    def test_create_contract(self):
        user = self.get_user()
        other_user = self.get_other_user()

        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_create_contract"):
            project_create = self.moco.Project.create(
                "dummy project, test contracts",
                "EUR",
                user.id,
                customer.id,
                finish_date=date(2020, 1, 1),
            )

            contract_create = self.moco.ProjectContract.create(
                project_create.data.id,
                other_user.id
            )

            project_get = self.moco.Project.get(project_create.data.id)

            assert project_create.response.status_code == 200
            assert contract_create.response.status_code == 200
            assert project_get.response.status_code == 200

            assert isinstance(project_create, JsonResponse)
            assert isinstance(contract_create, JsonResponse)
            assert isinstance(project_get, JsonResponse)

            assert contract_create.data.id in [x.id for x in project_get.data.contracts]

    def test_create_task(self):
        user = self.get_user()
        other_user = self.get_other_user()

        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_create_task"):
            project_create = self.moco.Project.create(
                "dummy project, test tasks",
                "EUR",
                user.id,
                customer.id,
                finish_date=date(2020, 1, 1),
            )

            task_create = self.moco.ProjectTask.create(
                project_create.data.id,
                "dummy task, test project with task",
            )

            project_get = self.moco.Project.get(project_create.data.id)

            assert project_create.response.status_code == 200
            assert task_create.response.status_code == 200
            assert project_get.response.status_code == 200

            assert isinstance(project_create, JsonResponse)
            assert isinstance(task_create, JsonResponse)
            assert isinstance(project_get, JsonResponse)

            assert task_create.data.id in [x.id for x in project_get.data.tasks]

    def test_getlist(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_getlist"):
            project_list = self.moco.Project.getlist(
                include_archived=True,
                include_company=True,
                leader_id=user.id,
                company_id=customer.id,
                created_from=date(2019, 1, 1),
                created_to=date(2021, 12, 31),
                updated_from=date(2019, 1, 1),
                updated_to=date(2021, 12, 31),
            )

            assert project_list.response.status_code == 200
            
            assert isinstance(project_list, ListingResponse)

    def test_assigned(self):
        with self.recorder.use_cassette("TestProject.test_assigned"):
            project_ass = self.moco.Project.assigned()

            assert project_ass.response.status_code == 200

            assert isinstance(project_ass, ListingResponse)

    def test_archive(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_archive"):
            project_create = self.moco.Project.create(
                "dummy project, test archive",
                "EUR",
                user.id,
                customer.id,
                finish_date = date(2020, 1, 1),
            )

            project_archive = self.moco.Project.archive(project_create.data.id)

            assert project_create.response.status_code == 200
            assert project_archive.response.status_code == 200

            assert isinstance(project_create, JsonResponse)
            assert isinstance(project_archive, JsonResponse)

            assert project_archive.data.active == False

    def test_unarchive(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_unarchive"):
            project_create = self.moco.Project.create(
                "dummy project, test unarchive",
                "EUR",
                user.id,
                customer.id,
                finish_date = date(2020, 1, 1),
            )

            project_archive = self.moco.Project.archive(project_create.data.id)
            project_unarchive = self.moco.Project.unarchive(project_create.data.id)

            assert project_create.response.status_code == 200
            assert project_archive.response.status_code == 200

            assert isinstance(project_create, JsonResponse)
            assert isinstance(project_archive, JsonResponse)

            assert project_archive.data.active == False
            assert project_unarchive.data.active == True

    def test_report(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_report"):
            project_create = self.moco.Project.create(
                "dummy project, test report",
                "EUR",
                user.id,
                customer.id,
                finish_date = date(2020, 1, 1),
            )
            
            project_report = self.moco.Project.report(project_create.data.id)

            assert project_create.response.status_code == 200
            assert project_report.response.status_code == 200

            assert isinstance(project_create, JsonResponse)
            assert isinstance(project_report, JsonResponse)

    def test_create_without_finish_date(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_create_without_finish_date"):
            name = "test project create"
            currency = "EUR"
            
            project_create = self.moco.Project.create(
                name,
                currency,
                user.id,
                customer.id,
            )

            assert project_create.response.status_code == 200

            assert isinstance(project_create, JsonResponse)

            assert project_create.data.name == name
            assert project_create.data.currency == currency
            assert project_create.data.finish_date is None
            assert project_create.data.leader.id == user.id
            assert project_create.data.customer.id == customer.id



    