from moco_wrapper.util.response import JsonResponse, ListingResponse, EmptyResponse

import string 
import random

from datetime import date
from .. import IntegrationTest

class TestProjectContract(IntegrationTest):
    def get_unit(self):
        with self.recorder.use_cassette("TestProjectContract.get_unit"):
            unit = self.moco.Unit.getlist().items[0]
            return unit
    
    def get_customer(self):
        with self.recorder.use_cassette("TestProjectContract.get_customer"):
            customer_create = self.moco.Company.create(
                "TestProjectContract",
                company_type="customer"
            )

            return customer_create.data
    
    def get_user(self):
        with self.recorder.use_cassette("TestProjectContract.get_user"):
            user = self.moco.User.getlist().items[0]
            return user

    def get_other_user(self):
        unit = self.get_unit()

        with self.recorder.use_cassette("TestProjectContract.get_other_user"):
            user_create = self.moco.User.create(
                "contract",
                "user",
                "{}@mycompany.com".format(self.id_generator()),
                self.id_generator(),
                unit.id,
                active=True,
            )

            return user_create.data


    def test_getlist(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProjectContract.test_getlist"):
            
            project_create = self.moco.Project.create(
                "dummy project, test contract getlist",
                "EUR",
                user.id,
                customer.id,
                finish_date = date(2020, 1, 1),  
            )

            contract_list = self.moco.ProjectContract.getlist(project_create.data.id)

            assert project_create.response.status_code == 200
            assert contract_list.response.status_code == 200
            
            assert isinstance(contract_list, ListingResponse)

    def test_create(self):
        user = self.get_user()
        customer = self.get_customer()
        other_user = self.get_other_user() #created user for assigning to project

        with self.recorder.use_cassette("TestProjectContract.test_create"):
            project_create = self.moco.Project.create(
                "dummy project, test contract create",
                "EUR",
                user.id,
                customer.id,
                finish_date = date(2020, 1, 1),
            )

            billable = False
            active = True
            budget = 9900
            hourly_rate = 100

            contract_create = self.moco.ProjectContract.create(
                project_create.data.id,
                other_user.id,
                billable=billable,
                active=active,
                budget=budget,
                hourly_rate=hourly_rate
            )

            assert project_create.response.status_code == 200
            assert contract_create.response.status_code == 200

            assert isinstance(project_create, JsonResponse)
            assert isinstance(contract_create, JsonResponse)
            
            assert contract_create.data.firstname == other_user.firstname
            assert contract_create.data.lastname == other_user.lastname
            assert contract_create.data.billable == billable
            assert contract_create.data.budget == budget
            assert contract_create.data.user_id == other_user.id
            assert contract_create.data.hourly_rate == hourly_rate
            assert contract_create.data.active == active

    def test_get(self):
        user = self.get_user()
        customer = self.get_customer()
        other_user = self.get_other_user() #created user for assigning to project

        with self.recorder.use_cassette("TestProjectContract.test_get"):
            project_create = self.moco.Project.create(
                "dummy project, test contract get",
                "EUR",
                user.id,
                customer.id,
                finish_date = date(2020, 1, 1),
            )

            billable = False
            active = True
            budget = 9900
            hourly_rate = 100

            contract_create = self.moco.ProjectContract.create(
                project_create.data.id,
                other_user.id,
                billable=billable,
                active=active,
                budget=budget,
                hourly_rate=hourly_rate
            )

            contract_get = self.moco.ProjectContract.get(
                project_create.data.id,
                contract_create.data.id
            )

            assert project_create.response.status_code == 200
            assert contract_create.response.status_code == 200
            assert contract_get.response.status_code == 200

            assert isinstance(project_create, JsonResponse)
            assert isinstance(contract_create, JsonResponse)
            assert isinstance(contract_get, JsonResponse)
            
            assert contract_get.data.firstname == other_user.firstname
            assert contract_get.data.lastname == other_user.lastname
            assert contract_get.data.billable == billable
            assert contract_get.data.budget == budget
            assert contract_get.data.user_id == other_user.id
            assert contract_get.data.hourly_rate == hourly_rate
            assert contract_get.data.active == active

    def test_update(self):
        user = self.get_user()
        customer = self.get_customer()
        other_user = self.get_other_user() #created user for assigning to project

        with self.recorder.use_cassette("TestProjectContract.test_update"):
            project_create = self.moco.Project.create(
                "dummy project, test contract update",
                "EUR",
                user.id,
                customer.id,
                finish_date = date(2020, 1, 1),
            )

            billable = False
            active = True
            budget = 9900.5
            hourly_rate = 100.2

            contract_create = self.moco.ProjectContract.create(
                project_create.data.id,
                other_user.id,
                billable=True,
                budget=1,
                hourly_rate=2,
            )

            contract_update = self.moco.ProjectContract.update(
                project_create.data.id,
                contract_create.data.id,
                billable=billable,
                active=active,
                budget=budget,
                hourly_rate=hourly_rate
            )

            assert project_create.response.status_code == 200
            assert contract_create.response.status_code == 200
            assert contract_update.response.status_code == 200

            assert isinstance(project_create, JsonResponse)
            assert isinstance(contract_create, JsonResponse)
            assert isinstance(contract_update, JsonResponse)
            
            assert contract_update.data.firstname == other_user.firstname
            assert contract_update.data.lastname == other_user.lastname
            assert contract_update.data.billable == billable
            assert contract_update.data.budget == budget
            assert contract_update.data.user_id == other_user.id
            assert contract_update.data.hourly_rate == hourly_rate
            assert contract_update.data.active == active

    def test_delete(self):
        user = self.get_user()
        customer = self.get_customer()
        other_user = self.get_other_user() #created user for assigning to project

        with self.recorder.use_cassette("TestProjectContract.test_delete"):
            project_create = self.moco.Project.create(
                "dummy project, test contract get",
                "EUR",
                user.id,
                customer.id,
                finish_date = date(2020, 1, 1),
            )

            billable = False
            active = True
            budget = 9900
            hourly_rate = 100

            contract_create = self.moco.ProjectContract.create(
                project_create.data.id,
                other_user.id,
                billable=billable,
                active=active,
                budget=budget,
                hourly_rate=hourly_rate
            )

            contract_delete = self.moco.ProjectContract.delete(
                project_create.data.id,
                contract_create.data.id
            )

            assert project_create.response.status_code == 200
            assert contract_create.response.status_code == 200
            assert contract_delete.response.status_code == 204

            assert isinstance(project_create, JsonResponse)
            assert isinstance(contract_create, JsonResponse)
            assert isinstance(contract_delete, EmptyResponse)