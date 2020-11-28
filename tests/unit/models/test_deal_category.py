from .. import UnitTest


class TestDealCategory(UnitTest):

    def test_create(self):
        name = "test deal category"
        prob = 15

        response = self.moco.DealCategory.create(
            name=name,
            probability=prob
        )

        data = response["data"]

        assert data["name"] == name
        assert data["probability"] == prob

        assert response["method"] == "POST"

    def test_update(self):
        cat_id = 22
        name = "test deal category to update"
        prob = 32

        response = self.moco.DealCategory.update(
            category_id=cat_id,
            name=name,
            probability=prob
        )

        data = response["data"]

        assert data["name"] == name
        assert data["probability"] == prob

        assert response["method"] == "PUT"

    def test_get(self):
        cat_id = 123

        response = self.moco.DealCategory.get(
            category_id=cat_id
        )

        assert response["method"] == "GET"

    def test_delete(self):
        cat_id = 22

        response = self.moco.DealCategory.delete(
            category_id=cat_id
        )

        assert response["method"] == "DELETE"
