from moco_wrapper.models.company import CompanyType
from moco_wrapper.models.tagging import TaggingEntity
from moco_wrapper.util.response import ListResponse

from .. import IntegrationTest


class TestTagging(IntegrationTest):

    def get_company(self):
        with self.recorder.use_cassette("TestTagging.get_company"):
            company_create = self.moco.Company.create(
                name="TestTagging Company",
                company_type=CompanyType.CUSTOMER
            )

            return company_create.data

    def test_get(self):
        company = self.get_company()

        with self.recorder.use_cassette("TestTagging.test_get"):
            tagging_get = self.moco.Tagging.get(
                entity=TaggingEntity.COMPANY,
                entity_id=company.id
            )

            assert tagging_get.response.status_code == 200

            assert type(tagging_get) is ListResponse

    def test_add(self):
        company = self.get_company()
        tags = ["test tagging", "add", "tags"]

        with self.recorder.use_cassette("TestTagging.test_add"):
            tagging_add = self.moco.Tagging.add(
                entity=TaggingEntity.COMPANY,
                entity_id=company.id,
                tags=tags
            )

            assert tagging_add.response.status_code == 200

            assert type(tagging_add) is ListResponse

            for tag in tags:
                assert tag in tagging_add.items

    def test_replace(self):
        company = self.get_company()
        tags = ["test tagging replace", "replace", "tags"]

        with self.recorder.use_cassette("TestTagging.test_replace"):
            tagging_replace = self.moco.Tagging.replace(
                entity=TaggingEntity.COMPANY,
                entity_id=company.id,
                tags=tags
            )
            assert tagging_replace.response.status_code == 200

            assert type(tagging_replace) is ListResponse

            assert sorted(tagging_replace.data) == sorted(tags)

    def test_delete(self):
        company = self.get_company()
        tags = ["test tagging delete", "delete", "tags"]

        with self.recorder.use_cassette("TestTagging.test_delete"):
            tagging_delete = self.moco.Tagging.delete(
                entity=TaggingEntity.COMPANY,
                entity_id=company.id,
                tags=tags
            )

            assert tagging_delete.response.status_code == 200

            assert type(tagging_delete) is ListResponse

            for tag in tags:
                assert tag not in tagging_delete.items
