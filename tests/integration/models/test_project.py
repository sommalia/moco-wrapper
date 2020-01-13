from moco_wrapper.util.response import JsonResponse, ListingResponse
from moco_wrapper.models.project import ProjectBillingVariant, ProjectCurrency

from datetime import date

from .. import IntegrationTest

class TestProject(IntegrationTest):
    def test_create(self):
        with self.recorder.use_cassette("TestProject.test_create"):
            user_get = self.moco.User.getlist().items[0]
            company_get = self.moco.Company.getlist().items[0]

            project_create = self.moco.Project.create("testproject name", ProjectCurrency.EUR, date(2020, 1, 1), user_get.id, company_get.id)

            assert project_create.response.status_code == 200

            assert isinstance(project_create, JsonResponse)

            assert project_create.data.name == "testproject name"
            assert project_create.data.finish_date == date(2020, 1, 1).isoformat()

    def test_create_with_budget(self):
        with self.recorder.use_cassette("TestProject.test_create_with_budget"):
            user_get = self.moco.User.getlist().items[0]
            company_get = self.moco.Company.getlist().items[0]

            project_budget = 300.5
            project_create = self.moco.Project.create("testproject name with budget", ProjectCurrency.EUR, date(2020, 1, 1), user_get.id, company_get.id, budget=project_budget)

            assert project_create.response.status_code == 200

            assert isinstance(project_create, JsonResponse)

            assert project_create.data.name == "testproject name with budget"
            assert project_create.data.finish_date == date(2020, 1, 1).isoformat()
            assert project_create.data.budget == project_budget

    def test_create_with_hourly_rate(self):
        with self.recorder.use_cassette("TestProject.test_create_with_hourly_rate"):
            user_get = self.moco.User.getlist().items[0]
            company_get = self.moco.Company.getlist().items[0]

            project_hourly_rate = 12.5
            project_create = self.moco.Project.create("testproject name, with hourly rate", ProjectCurrency.EUR, date(2020, 1, 1), user_get.id, company_get.id, hourly_rate=project_hourly_rate)

            assert project_create.response.status_code == 200

            assert isinstance(project_create, JsonResponse)

            assert project_create.data.name == "testproject name, with hourly rate"
            assert project_create.data.finish_date == date(2020, 1, 1).isoformat()
            assert project_create.data.hourly_rate == project_hourly_rate

    def test_create_with_labels(self):
        with self.recorder.use_cassette("TestProject.test_create_with_labels"):
            user_get = self.moco.User.getlist().items[0]
            company_get = self.moco.Company.getlist().items[0]

            project_labels = ["these", "are", "the", "labels"]
            project_create = self.moco.Project.create("testproject name, with labels", ProjectCurrency.EUR, date(2020, 1, 1), user_get.id, company_get.id, labels=project_labels )

            assert project_create.response.status_code == 200

            assert isinstance(project_create, JsonResponse)

            assert project_create.data.name == "testproject name, with labels"
            assert project_create.data.finish_date == date(2020, 1, 1).isoformat()
            assert sorted(project_create.data.labels) == sorted(project_labels)


    def test_update(self):
        with self.recorder.use_cassette("TestProject.test_update"):
            user_get = self.moco.User.getlist().items[0]
            company_get = self.moco.Company.getlist().items[0]

            project_create = self.moco.Project.create("testproject to update", ProjectCurrency.EUR, date(2000, 1, 1), user_get.id, company_get.id)
            project_update = self.moco.Project.update(project_create.data.id, name="updated name", finish_date=date(2021, 1, 1))

            assert project_create.response.status_code == 200 
            assert project_update.response.status_code == 200

            assert isinstance(project_update, JsonResponse)

            assert project_update.data.name == "updated name"
            assert project_update.data.finish_date == date(2021, 1, 1).isoformat()

    def test_get(self):
        with self.recorder.use_cassette("TestProject.test_get"):
            user_get = self.moco.User.getlist().items[0]
            company_get = self.moco.Company.getlist().items[0]

            project_create = self.moco.Project.create("testproject to get", ProjectCurrency.EUR, date(2000, 1, 1), user_get.id, company_get.id)
            project_get = self.moco.Project.get(project_create.data.id)

            assert project_create.response.status_code == 200
            assert project_get.response.status_code == 200

            assert isinstance(project_get, JsonResponse)

            assert project_get.data.name == "testproject to get"
            assert project_get.data.finish_date == date(2000, 1, 1).isoformat()

    def test_getlist(self):
        with self.recorder.use_cassette("TestProject.test_getlist"):
            project_getlist = self.moco.Project.getlist()

            assert project_getlist.response.status_code == 200

            assert isinstance(project_getlist, ListingResponse)

    def test_getlist_with_dates(self):
        with self.recorder.use_cassette("TestProject.test_getlist_with_dates"):
            created_from, created_to = date(2020, 1, 1), date(2020, 1, 1)
            updated_from, updated_to = date(2020, 1, 1), date(2020, 1, 1)

            project_getlist = self.moco.Project.getlist(created_from=created_from, created_to=created_to, updated_from=updated_from, updated_to=updated_to)

            assert project_getlist.response.status_code == 200
            assert isinstance(project_getlist, ListingResponse)

    def test_getlist_with_labels(self):
        with self.recorder.use_cassette("TestProject.test_getlist_with_labels"): 
            user_get = self.moco.User.getlist().items[0]
            company_get = self.moco.Company.getlist().items[0]
            project_create = self.moco.Project.create("test getlist with labels", ProjectCurrency.EUR, date(2020, 1, 1), user_get.id, company_get.id, labels=["important"])

            project_getlist = self.moco.Project.getlist(tags=["important"])

            assert project_create.response.status_code == 200
            assert project_getlist.response.status_code == 200

            assert isinstance(project_getlist, ListingResponse)

            for item in project_getlist.items:
                assert "important" in item.tags

    def test_assigned(self):
        with self.recorder.use_cassette("TestProject.test_assigned"):            
            project_assigned = self.moco.Project.assigned()

            assert project_assigned.response.status_code == 200

            assert isinstance(project_assigned, ListingResponse)

    def test_archive(self):
        with self.recorder.use_cassette("TestProject.test_archive"):
            user_get = self.moco.User.getlist().items[0]
            company_get = self.moco.Company.getlist().items[0]
            
            project_create = self.moco.Project.create("testproject to archive", ProjectCurrency.EUR, date(2020, 1, 1), user_get.id, company_get.id)
            project_archive = self.moco.Project.archive(project_create.data.id)
            project_get = self.moco.Project.get(project_create.data.id)

            assert project_create.response.status_code == 200
            assert project_archive.response.status_code == 200
            assert project_get.response.status_code == 200

            assert isinstance(project_archive, JsonResponse)
            
            assert project_create.data.active == True
            assert project_get.data.active == False

    def test_unarchive(self):
       with self.recorder.use_cassette("TestProject.test_unarchive"):
            user_get = self.moco.User.getlist().items[0]
            company_get = self.moco.Company.getlist().items[0]
            
            project_create = self.moco.Project.create("testproject to unarchive", ProjectCurrency.EUR, date(2020, 1, 1), user_get.id, company_get.id)
            project_archive = self.moco.Project.archive(project_create.data.id)
            project_get = self.moco.Project.get(project_create.data.id)

            project_unarchive = self.moco.Project.unarchive(project_create.data.id)

            assert project_create.response.status_code == 200
            assert project_archive.response.status_code == 200
            assert project_get.response.status_code == 200
            assert project_unarchive.response.status_code == 200

            assert isinstance(project_unarchive, JsonResponse)
            
            assert project_create.data.active == True
            assert project_get.data.active == False
            assert project_unarchive.data.active == True

    def test_report(self):
        with self.recorder.use_cassette("TestProject.test_report"):
            user_get = self.moco.User.getlist().items[0]
            company_get = self.moco.Company.getlist().items[0]
            
            project_create = self.moco.Project.create("testproject to report", ProjectCurrency.EUR, date(2020, 1, 1), user_get.id, company_get.id)
            
            project_report = self.moco.Project.report(project_create.data.id)

            assert project_report.response.status_code == 200
            
            assert isinstance(project_report, JsonResponse)
