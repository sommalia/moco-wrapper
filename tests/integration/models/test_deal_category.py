from moco_wrapper.util.response import JsonResponse, ListingResponse, ErrorResponse, EmptyResponse

from .. import IntegrationTest

class TestDealCategory(IntegrationTest):
    def test_create(self):
        with self.recorder.use_cassette("TestDealCategory.test_create"):
            r = self.moco.DealCategory.create("this is a new category", 1)

            assert r.data.probability == 1
            assert r.response.status_code == 200
            assert isinstance(r, JsonResponse)

    def test_create_with_prob_over_100(self):
        with self.recorder.use_cassette("TestDealCategory.test_create_with_prob_over_100"):
            r = self.moco.DealCategory.create("this is another category", 120)
            assert isinstance(r, ErrorResponse)

    def test_update(self):
        with self.recorder.use_cassette("TestDealCategory.test_update"):
            create_r = self.moco.DealCategory.create("this category is to update", 50)
            update_r = self.moco.DealCategory.update(create_r.data.id, probability=66)

            assert isinstance(update_r, JsonResponse) 
            assert update_r.data.probability == 66
            assert update_r.response.status_code == 200
            

    def test_get(self):
        with self.recorder.use_cassette("TestDealCategory.test_get"):
            create_r = self.moco.DealCategory.create("this category is to get", 50)
            print(create_r)
            get_r = self.moco.DealCategory.get(create_r.data.id)

            assert isinstance(get_r, JsonResponse) 
            assert get_r.data.probability == 50
            assert get_r.response.status_code == 200

    def test_getlist(self):
        with self.recorder.use_cassette("TestDealCategory.test_getlist"):
            r = self.moco.DealCategory.getlist()

            assert isinstance(r, ListingResponse) 
            assert r.response.status_code == 200

    def test_delete(self):
        with self.recorder.use_cassette("TestDealCategory.test_delete"):
            create_r = self.moco.DealCategory.create("this is a category to delete", 1)
            delete_r = self.moco.DealCategory.delete(create_r.data.id)

            assert isinstance(delete_r, EmptyResponse) 
            assert delete_r.response.status_code == 204