import pytest
from .. import UnitTest


class TestProject(UnitTest):

    def test_create(self):
        name = "custom boards 200000"
        currency = "EUR"
        finish_date = "2019-05-15"
        leader_id = 4123
        customer_id = 4
        deal_id = 834
        identifier = "PROJ-4"
        billing_address = "this is the billing address"
        billing_variant = "project"
        hourly_rate = 124
        budget = 120000
        labels = ["this", "is", "my", "board"]
        custom_properties = {
            "boards": 14
        }
        info = "more information about boards"

        response = self.moco.Project.create(
            name=name,
            currency=currency,
            leader_id=leader_id,
            customer_id=customer_id,
            deal_id=deal_id,
            finish_date=finish_date,
            identifier=identifier,
            billing_address=billing_address,
            billing_variant=billing_variant,
            hourly_rate=hourly_rate,
            budget=budget,
            labels=labels,
            custom_properties=custom_properties,
            info=info
        )
        data = response["data"]

        assert data["name"] == name
        assert data["currency"] == currency
        assert data["finish_date"] == finish_date
        assert data["leader_id"] == leader_id
        assert data["customer_id"] == customer_id
        assert data["deal_id"] == deal_id
        assert data["billing_address"] == billing_address
        assert data["billing_variant"] == billing_variant
        assert data["hourly_rate"] == hourly_rate
        assert data["labels"] == labels
        assert data["custom_properties"] == custom_properties
        assert data["info"] == info

        assert response["method"] == "POST"

    def test_update(self):
        project_id = 213
        name = "custom boards 200000"
        finish_date = "2019-05-15"
        leader_id = 4123
        customer_id = 4
        deal_id = 231
        identifier = "PROJ-4"
        billing_address = "this is the billing address"
        billing_variant = "project"
        hourly_rate = 124
        budget = 120000
        labels = ["this", "is", "my", "board"]
        custom_properties = {
            "boards": 14
        }
        info = "more information about boards"

        response = self.moco.Project.update(
            project_id=project_id,
            name=name,
            finish_date=finish_date,
            leader_id=leader_id,
            customer_id=customer_id,
            deal_id=deal_id,
            identifier=identifier,
            billing_address=billing_address,
            billing_variant=billing_variant,
            hourly_rate=hourly_rate,
            budget=budget,
            labels=labels,
            custom_properties=custom_properties,
            info=info
        )
        data = response["data"]

        assert data["name"] == name
        assert data["finish_date"] == finish_date
        assert data["leader_id"] == leader_id
        assert data["customer_id"] == customer_id
        assert data["deal_id"] == deal_id
        assert data["billing_address"] == billing_address
        assert data["billing_variant"] == billing_variant
        assert data["hourly_rate"] == hourly_rate
        assert data["labels"] == labels
        assert data["custom_properties"] == custom_properties
        assert data["info"] == info

        assert response["method"] == "PUT"

    def test_get(self):
        project_id = 2314

        response = self.moco.Project.get(project_id)

        assert response["method"] == "GET"

    def test_getlist(self):
        include_archived = False
        include_company = True
        leader_id = 34
        company_id = 43
        created_from = '2019-01-01'
        created_to = '2019-10-10'
        updated_from = '2015-01-01'
        updated_to = '2015-05-05'
        tags = ["these", "are", "my", "tags"]
        identifier = "PROJ-IAM-SEARCHING"

        response = self.moco.Project.getlist(include_archived=include_archived, include_company=include_company,
                                             leader_id=leader_id, company_id=company_id, created_from=created_from,
                                             created_to=created_to, updated_from=updated_from, updated_to=updated_to,
                                             tags=tags, identifier=identifier)
        params = response["params"]

        assert params["include_archived"] == include_archived
        assert params["include_company"] == include_company
        assert params["leader_id"] == leader_id
        assert params["company_id"] == company_id
        assert params["created_from"] == created_from
        assert params["created_to"] == created_to
        assert params["updated_from"] == updated_from
        assert params["updated_to"] == updated_to
        assert params["tags"] == tags
        assert params["identifier"] == identifier

        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        sort_by = "test field to sort by"

        response = self.moco.Project.getlist(sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_getlist_sort_overwrite(self):
        sort_by = "test field to sort by"
        sort_order = "desc"

        response = self.moco.Project.getlist(sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        page_default = 1

        response = self.moco.Project.getlist()
        assert response["params"]["page"] == page_default

    def test_getlist_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.Project.getlist(page=page_overwrite)
        assert response["params"]["page"] == page_overwrite

    def test_assigned(self):
        active = False

        response = self.moco.Project.assigned(active=active)

        assert response["params"]["active"] == active

    def test_assigned_sort_default(self):
        sort_by = "test field to sort by"

        response = self.moco.Project.assigned(sort_by=sort_by)

        assert response["params"]["sort_by"] == "{} asc".format(sort_by)

    def test_assigned_sort_overwrite(self):
        sort_by = "test field to sort by"
        sort_order = "desc"

        response = self.moco.Project.assigned(sort_by=sort_by, sort_order=sort_order)

        assert response["params"]["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_assigned_page_default(self):
        page_default = 1

        response = self.moco.Project.assigned()
        assert response["params"]["page"] == page_default

    def test_assigned_page_overwrite(self):
        page_overwrite = 22

        response = self.moco.Project.assigned(page=page_overwrite)
        assert response["params"]["page"] == page_overwrite

    def test_archive(self):
        project_id = 123

        response = self.moco.Project.archive(project_id)

        assert response["method"] == "PUT"

    def test_unarchive(self):
        project_id = 123

        response = self.moco.Project.unarchive(project_id)

        assert response["method"] == "PUT"

    def test_report(self):
        project_id = 123

        response = self.moco.Project.report(project_id)

        assert response["method"] == "GET"
