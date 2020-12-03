import pytest
from .. import UnitTest


class TestProjectContract(UnitTest):

    def test_create(self):
        project_id = 2
        user_id = 4

        billable = False
        active = True
        budget = 10000
        hourly_rate = 2100

        response = self.moco.ProjectContract.create(
            project_id=project_id,
            user_id=user_id,
            billable=billable,
            active=active,
            budget=budget,
            hourly_rate=hourly_rate
        )

        data = response["data"]

        assert data["billable"] == billable
        assert data["active"] == active
        assert data["budget"] == budget
        assert data["hourly_rate"] == hourly_rate

        assert response["method"] == "POST"

    def test_update(self):
        project_id = 2
        contract_id = 3

        billable = False
        active = True
        budget = 10000
        hourly_rate = 2100

        response = self.moco.ProjectContract.update(
            project_id=project_id,
            contract_id=contract_id,
            billable=billable,
            active=active,
            budget=budget,
            hourly_rate=hourly_rate
        )

        data = response["data"]

        assert data["billable"] == billable
        assert data["active"] == active
        assert data["budget"] == budget
        assert data["hourly_rate"] == hourly_rate

        assert response["method"] == "PUT"

    def test_get(self):
        project_id = 2
        contract_id = 222

        response = self.moco.ProjectContract.get(
            project_id=project_id,
            contract_id=contract_id
        )

        assert response["method"] == "GET"

    def test_getlist(self):
        project_id = 2

        response = self.moco.ProjectContract.getlist(
            project_id=project_id
        )

        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        project_id = 2
        sort_by = "field to sort by"

        response = self.moco.ProjectContract.getlist(
            project_id=project_id,
            sort_by=sort_by
        )

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        project_id = 2
        sort_by = "field to sort by"
        sort_order = "desc"

        response = self.moco.ProjectContract.getlist(
            project_id=project_id,
            sort_by=sort_by,
            sort_order=sort_order
        )

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        project_id = 1
        page_default = 1

        response = self.moco.ProjectContract.getlist(
            project_id=project_id
        )

        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        project_id = 1
        page_overwrite = 22

        response = self.moco.ProjectContract.getlist(
            project_id=project_id,
            page=page_overwrite
        )

        assert response["params"]["page"] == page_overwrite

    def test_delete(self):
        project_id = 1
        contract_id = 2

        response = self.moco.ProjectContract.delete(
            project_id=project_id,
            contract_id=contract_id
        )

        assert response["method"] == "DELETE"
