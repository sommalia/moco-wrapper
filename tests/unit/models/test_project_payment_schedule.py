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

        response = self.moco.ProjectPaymentSchedule.getlist(
            project_id=project_id,
        )

        assert response["method"] == "GET"
