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
            project_id,
            net_total,
            sched_date,
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
            project_id,
            schedule_id,
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
            project_id,
            schedule_id,
        )

        assert response["method"] == "DELETE"

    def test_get(self):
        project_id = 1
        schedule_id = 2

        response = self.moco.ProjectPaymentSchedule.get(
            project_id,
            schedule_id,
        )

        assert response["method"] == "GET"

    def test_getlist(self):
        project_id = 1

        response = self.moco.ProjectPaymentSchedule.getlist(
            project_id,
        )

        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        project_id = 2
        sort_by = "field to sort by"

        response = self.moco.ProjectPaymentSchedule.getlist(project_id, sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        project_id = 2
        sort_by = "field to sort by"
        sort_order = "desc"

        response = self.moco.ProjectPaymentSchedule.getlist(project_id, sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        project_id = 1
        page_default = 1

        response = self.moco.ProjectPaymentSchedule.getlist(project_id)
        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        project_id = 1
        page_overwrite = 22

        response = self.moco.ProjectPaymentSchedule.getlist(project_id, page=page_overwrite)
        assert response["params"]["page"] == page_overwrite
