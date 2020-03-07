from moco_wrapper.util.response import JsonResponse, ListingResponse, ErrorResponse, EmptyResponse

import string
import random

from .. import IntegrationTest

class TestDealCategory(IntegrationTest):
    def test_create(self):
        with self.recorder.use_cassette("TestDealCategory.test_create"):
            name = self.id_generator()
            probability = 1
            
            cat_create = self.moco.DealCategory.create(
                name,
                probability
            )

            assert cat_create.response.status_code == 200

            assert isinstance(cat_create, JsonResponse)      
            
            assert cat_create.data.name is not None
            assert cat_create.data.probability == probability
            

    def test_update(self):
        with self.recorder.use_cassette("TestDealCategory.test_update"):
            name = self.id_generator()
            probability = 50
            
            cat_create = self.moco.DealCategory.create(
                self.id_generator(),
                1
            )
            cat_update = self.moco.DealCategory.update(
                cat_create.data.id,
                name=name,
                probability=probability)

            assert cat_create.response.status_code == 200
            assert cat_update.response.status_code == 200

            assert isinstance(cat_update, JsonResponse) 

            assert cat_update.data.name is not None
            assert cat_update.data.probability == probability
            

    def test_get(self):
        with self.recorder.use_cassette("TestDealCategory.test_get"):
            name = self.id_generator()
            probability = 77


            cat_create = self.moco.DealCategory.create(
                name,
                probability
            )
            cat_get = self.moco.DealCategory.get(cat_create.data.id)

            assert cat_create.response.status_code == 200
            assert cat_get.response.status_code == 200

            assert isinstance(cat_get, JsonResponse) 

            assert cat_get.data.name is not None
            assert cat_get.data.probability == probability
            

    def test_getlist(self):
        with self.recorder.use_cassette("TestDealCategory.test_getlist"):
            cat_getlist = self.moco.DealCategory.getlist()

            assert cat_getlist.response.status_code == 200

            assert isinstance(cat_getlist, ListingResponse) 

            assert cat_getlist.current_page == 1
            assert cat_getlist.is_last is not None
            assert cat_getlist.next_page is not None
            assert cat_getlist.total is not None
            assert cat_getlist.page_size is not None

    def test_delete(self):
        with self.recorder.use_cassette("TestDealCategory.test_delete"):
            cat_create = self.moco.DealCategory.create(
                self.id_generator(),
                1
            )
            cat_delete = self.moco.DealCategory.delete(cat_create.data.id)

            assert cat_create.response.status_code == 200
            assert cat_delete.response.status_code == 204

            assert isinstance(cat_delete, EmptyResponse) 
            