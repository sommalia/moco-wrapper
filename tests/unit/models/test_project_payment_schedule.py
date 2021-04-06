from .. import UnitTest
import pytest


class TestProjectPaymentSchedule(UnitTest):
    def test_create(self):
        project_id = 1
        net_total = 22
        sched_date = "2020-01-01"
        title = "this is the title"
        checked = False

        response = self.moco.ProjectPaymentSchedule.create(
            project_id=project_id,
            net_total=net_total,
            schedule_date=sched_date,
            title=title,
            checked=checked
        )

        data = response["data"]

        assert response["method"] == "POST"

        assert data["net_total"] == net_total
        assert data["date"] == sched_date
        assert data["title"] == title
        assert data["checked"] == checked

    def test_update(self):
        project_id = 1
        schedule_id = 2
        net_total = 22
        sched_date = "2020-01-01"
        title = "this is the title"
        checked = False

        response = self.moco.ProjectPaymentSchedule.update(
            project_id=project_id,
            schedule_id=schedule_id,
            net_total=net_total,
            schedule_date=sched_date,
            title=title,
            checked=checked
        )

        data = response["data"]

        assert response["method"] == "PUT"

        assert data["net_total"] == net_total
        assert data["date"] == sched_date
        assert data["title"] == title
        assert data["checked"] == checked

    def test_delete(self):
        project_id = 1
        schedule_id = 2

        response = self.moco.ProjectPaymentSchedule.delete(
            project_id=project_id,
            schedule_id=schedule_id,
        )

        assert response["method"] == "DELETE"

    def test_get(self):
        project_id = 1
        schedule_id = 2

        response = self.moco.ProjectPaymentSchedule.get(
            project_id=project_id,
            schedule_id=schedule_id,
        )

        assert response["method"] == "GET"

    def test_getlist(self):
        project_id = 1
        from_date = "2021-02-03"
        to_date = "2022-03-22"
        checked = False

        response = self.moco.ProjectPaymentSchedule.getlist(
            project_id=project_id,
            from_date=from_date,
            to_date=to_date,
            checked=checked
        )

        params = response["params"]

        assert response["method"] == "GET"

        assert params["from"] == from_date
        assert params["to"] == to_date
        assert params["checked"] == checked


    def test_getall(self):
        project_id = 2
        company_id = 44
        from_date = "2021-01-01"
        to_date = "2023-03-24"
        checked = True

        response = self.moco.ProjectPaymentSchedule.getall(
            from_date=from_date,
            to_date=to_date,
            checked=checked,
            company_id=company_id,
            project_id=project_id
        )

        params = response["params"]

        assert response["method"] == "GET"

        assert params["from"] == from_date
        assert params["to"] == to_date
        assert params["checked"] == checked
        assert params["company_id"] == company_id
        assert params["project_id"] == project_id
