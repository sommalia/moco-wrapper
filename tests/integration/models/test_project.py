from moco_wrapper.util.response import ObjectResponse, PagedListResponse, ListResponse, EmptyResponse
from moco_wrapper.models.project import ProjectBillingVariant
from moco_wrapper.models.company import CompanyType

from datetime import date

from .. import IntegrationTest


class TestProject(IntegrationTest):
    def get_unit(self):
        with self.recorder.use_cassette("TestProject.get_unit"):
            unit = self.moco.Unit.getlist()[0]
            return unit

    def get_user(self):
        with self.recorder.use_cassette("TestProject.get_user"):
            user = self.moco.User.getlist()[0]
            return user

    def get_other_user(self):
        unit = self.get_unit()

        with self.recorder.use_cassette("TestProject.get_other_user"):
            user_create = self.moco.User.create(
                firstname="-",
                lastname="TestProject.get_other_user",
                email="{}@example.org".format(self.id_generator()),
                password=self.id_generator(),
                unit_id=unit.id,
            )

            return user_create.data

    def get_customer(self):
        with self.recorder.use_cassette("TestProject.get_customer"):
            customer_create = self.moco.Company.create(
                name="TestProject.get_customer",
                company_type=CompanyType.CUSTOMER
            )

            return customer_create.data

    def get_deal_category(self):
        with self.recorder.use_cassette("TestProject.get_deal_category"):
            deal_category = self.moco.DealCategory.getlist()[0]

            return deal_category

    def get_deal(self):
        category = self.get_deal_category()
        user = self.get_user()

        with self.recorder.use_cassette("TestProject.get_deal"):
            deal_create = self.moco.Deal.create(
                name="TestProject.get_deal",
                currency="EUR",
                money=100,
                reminder_date=date(2021, 1, 1),
                user_id=user.id,
                deal_category_id=category.id
            )

            return deal_create.data

    def test_create(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_create"):
            name = "TestProject.test_create"
            currency = "EUR"
            finish_date = date(2021, 1, 1)

            project_create = self.moco.Project.create(
                name=name,
                currency=currency,
                leader_id=user.id,
                customer_id=customer.id,
                finish_date=finish_date
            )

            assert project_create.response.status_code == 200

            assert type(project_create) is ObjectResponse

            assert project_create.data.name == name
            assert project_create.data.currency == currency
            assert project_create.data.finish_date == finish_date.isoformat()
            assert project_create.data.leader.id == user.id
            assert project_create.data.customer.id == customer.id

    def test_create_with_deal(self):
        user = self.get_user()
        customer = self.get_customer()
        deal = self.get_deal()

        with self.recorder.use_cassette("TestProject.test_create_with_deal"):
            name = "TestProject.test_create_with_deal"
            currency = "EUR"

            project_create = self.moco.Project.create(
                name=name,
                currency=currency,
                leader_id=user.id,
                customer_id=customer.id,
                deal_id=deal.id
            )

            assert project_create.response.status_code == 200

            assert type(project_create) is ObjectResponse

            assert project_create.data.name == name
            assert project_create.data.currency == currency
            assert project_create.data.leader.id == user.id
            assert project_create.data.customer.id == customer.id
            assert project_create.data.deal.id == deal.id

    def test_create_full(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_create_full"):
            name = "TestProject.test_create_full"
            currency = "EUR"
            finish_date = date(2021, 1, 1)
            billing_address = "general street 22"
            billing_email_to = "billing@example.org"
            billing_email_cc = "billing-cc@example.org"
            billing_notes = "billing notes text"
            setting_include_time_report = True
            billing_variant = ProjectBillingVariant.PROJECT
            hourly_rate = 12.5
            budget = 100
            tags = ["low risk", "low income"]
            info = "general information"

            project_create = self.moco.Project.create(
                name=name,
                currency=currency,
                leader_id=user.id,
                customer_id=customer.id,
                finish_date=finish_date,
                billing_address=billing_address,
                billing_email_to=billing_email_to,
                billing_email_cc=billing_email_cc,
                billing_notes=billing_notes,
                setting_include_time_report=setting_include_time_report,
                billing_variant=billing_variant,
                hourly_rate=hourly_rate,
                budget=budget,
                tags=tags,
                info=info
            )

            assert project_create.response.status_code == 200

            assert type(project_create) is ObjectResponse

            assert project_create.data.name == name
            assert project_create.data.currency == currency
            assert project_create.data.finish_date == finish_date.isoformat()
            assert project_create.data.leader.id == user.id
            assert project_create.data.customer.id == customer.id
            assert project_create.data.billing_address == billing_address
            assert project_create.data.billing_email_to == billing_email_to
            assert project_create.data.billing_email_cc == billing_email_cc
            assert project_create.data.billing_notes == billing_notes
            assert project_create.data.setting_include_time_report == setting_include_time_report
            assert project_create.data.billing_variant == billing_variant
            assert project_create.data.hourly_rate == hourly_rate
            assert project_create.data.budget == budget
            assert sorted(project_create.data.tags) == sorted(tags)
            assert project_create.data.info == info

    def test_get(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_get"):
            name = "TestProject.test_get_create"
            currency = "EUR"
            finish_date = date(2021, 1, 1)
            billing_address = "general street 22"
            billing_variant = ProjectBillingVariant.PROJECT
            hourly_rate = 12.5
            budget = 100
            tags = ["low risk", "low income"]
            info = "general information"

            project_create = self.moco.Project.create(
                name=name,
                currency=currency,
                leader_id=user.id,
                customer_id=customer.id,
                finish_date=finish_date,
                billing_address=billing_address,
                billing_variant=billing_variant,
                hourly_rate=hourly_rate,
                budget=budget,
                tags=tags,
                info=info
            )

            project_get = self.moco.Project.get(project_create.data.id)

            assert project_create.response.status_code == 200
            assert project_get.response.status_code == 200

            assert type(project_create) is ObjectResponse
            assert type(project_get) is ObjectResponse

            assert project_get.data.name == name
            assert project_get.data.currency == currency
            assert project_get.data.finish_date == finish_date.isoformat()
            assert project_get.data.leader.id == user.id
            assert project_get.data.customer.id == customer.id
            assert project_get.data.billing_address == billing_address
            assert project_get.data.billing_variant == billing_variant
            assert project_get.data.hourly_rate == hourly_rate
            assert project_get.data.budget == budget
            assert sorted(project_get.data.tags) == sorted(tags)
            assert project_get.data.info == info

    def test_update(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_update"):
            name = "TestProject.test_update"
            currency = "EUR"
            finish_date = date(2021, 1, 1)
            billing_address = "general street 22"
            billing_email_to = "billing-update@example.org"
            billing_email_cc = "billing-cc-update@example.org"
            billing_notes = "billings notes update text"
            setting_include_time_report = False
            billing_variant = ProjectBillingVariant.PROJECT
            hourly_rate = 12.5
            budget = 100
            tags = ["low risk", "low income"]
            info = "general information"

            project_create = self.moco.Project.create(
                name="TestProject.test_update_create",
                currency="EUR",
                leader_id=user.id,
                customer_id=customer.id,
                finish_date=date(2020, 1, 1),
            )

            project_update = self.moco.Project.update(
                project_id=project_create.data.id,
                name=name,
                finish_date=finish_date,
                leader_id=user.id,
                customer_id=customer.id,
                billing_address=billing_address,
                billing_email_to=billing_email_to,
                billing_email_cc=billing_email_cc,
                billing_notes=billing_notes,
                setting_include_time_report=setting_include_time_report,
                billing_variant=billing_variant,
                hourly_rate=hourly_rate,
                budget=budget,
                tags=tags,
                info=info
            )

            assert project_create.response.status_code == 200
            assert project_update.response.status_code == 200

            assert type(project_create) is ObjectResponse
            assert type(project_update) is ObjectResponse

            assert project_update.data.name == name
            assert project_update.data.currency == currency
            assert project_update.data.finish_date == finish_date.isoformat()
            assert project_update.data.leader.id == user.id
            assert project_update.data.customer.id == customer.id
            assert project_update.data.billing_address == billing_address
            assert project_update.data.billing_email_to == billing_email_to
            assert project_update.data.billing_email_cc == billing_email_cc
            assert project_update.data.billing_notes == billing_notes
            assert project_update.data.setting_include_time_report == setting_include_time_report
            assert project_update.data.billing_variant == billing_variant
            assert project_update.data.hourly_rate == hourly_rate
            assert project_update.data.budget == budget
            assert sorted(project_update.data.tags) == sorted(tags)
            assert project_update.data.info == info

    def test_create_contract(self):
        user = self.get_user()
        other_user = self.get_other_user()

        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_create_contract"):
            project_create = self.moco.Project.create(
                name="TestProject.test_create_contract_create",
                currency="EUR",
                leader_id=user.id,
                customer_id=customer.id,
                finish_date=date(2020, 1, 1),
            )

            contract_create = self.moco.ProjectContract.create(
                project_id=project_create.data.id,
                user_id=other_user.id
            )

            project_get = self.moco.Project.get(project_create.data.id)

            assert project_create.response.status_code == 200
            assert contract_create.response.status_code == 200
            assert project_get.response.status_code == 200

            assert type(project_create) is ObjectResponse
            assert type(contract_create) is ObjectResponse
            assert type(project_get) is ObjectResponse

            assert contract_create.data.id in [x.id for x in project_get.data.contracts]

    def test_create_task(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_create_task"):
            project_create = self.moco.Project.create(
                name="TestProject.test_create_task_create",
                currency="EUR",
                leader_id=user.id,
                customer_id=customer.id,
                finish_date=date(2020, 1, 1),
            )

            task_create = self.moco.ProjectTask.create(
                project_id=project_create.data.id,
                name="TestProject.test_create_task_task_create",
            )

            project_get = self.moco.Project.get(project_create.data.id)

            assert project_create.response.status_code == 200
            assert task_create.response.status_code == 200
            assert project_get.response.status_code == 200

            assert type(project_create) is ObjectResponse
            assert type(task_create) is ObjectResponse
            assert type(project_get) is ObjectResponse

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

            assert type(project_list) is PagedListResponse

            assert project_list.current_page == 1
            assert project_list.is_last is not None
            assert project_list.next_page is not None
            assert project_list.total is not None
            assert project_list.page_size is not None

    def test_assigned(self):
        with self.recorder.use_cassette("TestProject.test_assigned"):
            project_ass = self.moco.Project.assigned()

            assert project_ass.response.status_code == 200

            assert type(project_ass) is ListResponse

    def test_archive(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_archive"):
            project_create = self.moco.Project.create(
                name="TestProject.test_archive_create",
                currency="EUR",
                leader_id=user.id,
                customer_id=customer.id,
                finish_date=date(2020, 1, 1),
            )

            project_archive = self.moco.Project.archive(project_create.data.id)

            assert project_create.response.status_code == 200
            assert project_archive.response.status_code == 200

            assert type(project_create) is ObjectResponse
            assert type(project_archive) is ObjectResponse

            assert not project_archive.data.active

    def test_unarchive(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_unarchive"):
            project_create = self.moco.Project.create(
                name="TestProject.test_unarchive_create",
                currency="EUR",
                leader_id=user.id,
                customer_id=customer.id,
                finish_date=date(2020, 1, 1),
            )

            project_archive = self.moco.Project.archive(project_create.data.id)
            project_unarchive = self.moco.Project.unarchive(project_create.data.id)

            assert project_create.response.status_code == 200
            assert project_archive.response.status_code == 200

            assert type(project_create) is ObjectResponse
            assert type(project_archive) is ObjectResponse

            assert not project_archive.data.active
            assert project_unarchive.data.active

    def test_report(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_report"):
            project_create = self.moco.Project.create(
                name="TestProject.test_report_create",
                currency="EUR",
                leader_id=user.id,
                customer_id=customer.id,
                finish_date=date(2020, 1, 1),
            )

            project_report = self.moco.Project.report(project_create.data.id)

            assert project_create.response.status_code == 200
            assert project_report.response.status_code == 200

            assert type(project_create) is ObjectResponse
            assert type(project_report) is ObjectResponse

    def test_create_without_finish_date(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_create_without_finish_date"):
            name = "TestProject.test_create_without_finish_date_create"
            currency = "EUR"

            project_create = self.moco.Project.create(
                name=name,
                currency=currency,
                leader_id=user.id,
                customer_id=customer.id,
            )

            assert project_create.response.status_code == 200

            assert type(project_create) is ObjectResponse

            assert project_create.data.name == name
            assert project_create.data.currency == currency
            assert project_create.data.finish_date is None
            assert project_create.data.leader.id == user.id
            assert project_create.data.customer.id == customer.id

    def test_create_fixed_price(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_create_fixed_price"):
            name = "TestProject.test_create_fixed_price_create"
            currency = "EUR"
            budget = 200
            fixed_price = True

            project_create = self.moco.Project.create(
                name=name,
                currency=currency,
                leader_id=user.id,
                customer_id=customer.id,
                fixed_price=fixed_price,
                budget=200
            )

            assert project_create.response.status_code == 200

            assert type(project_create) is ObjectResponse

            assert project_create.data.name == name
            assert project_create.data.currency == currency
            assert project_create.data.finish_date is None
            assert project_create.data.leader.id == user.id
            assert project_create.data.customer.id == customer.id
            assert project_create.data.budget == budget
            assert project_create.data.fixed_price == fixed_price


    def test_destroy(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProject.test_delete"):

            project_create = self.moco.Project.create(
                name="TestProject.test_delete_create",
                currency="EUR",
                leader_id=user.id,
                customer_id=customer.id,
                finish_date=date(2020, 1, 1),
            )

            project_delete = self.moco.Project.destroy(
                project_id=project_create.data.id
            )

            assert project_create.response.status_code == 200
            assert project_delete.response.status_code == 200

            assert type(project_create) is ObjectResponse
            assert type(project_delete) is EmptyResponse
