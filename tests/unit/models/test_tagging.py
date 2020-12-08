import pytest

from .. import UnitTest
from moco_wrapper.models.tagging import TaggingEntity


class TestTagging(UnitTest):

    def test_get(self):
        entity = TaggingEntity.CONTACT
        entity_id = 23

        response = self.moco.Tagging.get(
            entity=entity,
            entity_id=entity_id
        )

        url_parts = response["path"].split("/")

        assert url_parts[-1] == str(entity_id)
        assert url_parts[-2] == entity
        assert response["method"] == "GET"

    def test_add(self):
        entity = TaggingEntity.PROJECT
        entity_id = 22
        tags = ["list", "example", "tags"]

        response = self.moco.Tagging.add(
            entity=entity,
            entity_id=entity_id,
            tags=tags
        )

        data = response["data"]
        url_parts = response["path"].split("/")

        assert url_parts[-1] == str(entity_id)
        assert url_parts[-2] == entity
        assert data["tags"] == tags
        assert response["method"] == "PATCH"

    def test_replace(self):
        entity = TaggingEntity.OFFER
        entity_id = 335
        tags = ["other", "tag list"]

        response = self.moco.Tagging.replace(
            entity=entity,
            entity_id=entity_id,
            tags=tags
        )

        data = response["data"]
        url_parts = response["path"].split("/")

        assert url_parts[-1] == str(entity_id)
        assert url_parts[-2] == entity
        assert data["tags"] == tags
        assert response["method"] == "PUT"

    def test_delete(self):
        entity = TaggingEntity.COMPANY
        entity_id = 4234
        tags = ["important", "high-value"]

        response = self.moco.Tagging.delete(
            entity=entity,
            entity_id=entity_id,
            tags=tags
        )

        data = response["data"]
        url_parts = response["path"].split("/")

        assert url_parts[-1] == str(entity_id)
        assert url_parts[-2] == entity
        assert data["tags"] == tags
        assert response["method"] == "DELETE"

