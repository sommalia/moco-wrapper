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