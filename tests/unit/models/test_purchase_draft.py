from .. import UnitTest


class TestPurchaseDraft(UnitTest):

    def test_get(self):
        draft_id = 1

        response = self.moco.PurchaseDraft.get(draft_id=draft_id)

        assert response["method"] == "GET"

    def test_pdf(self):
        draft_id = 1

        response = self.moco.PurchaseDraft.pdf(draft_id=draft_id)

        assert response["method"] == "GET"

    def test_getlist(self):
        response = self.moco.PurchaseDraft.getlist()

        assert response["method"] == "GET"
