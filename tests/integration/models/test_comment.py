from moco_wrapper.models.comment import CommentTargetType
from moco_wrapper.util.response import ListingResponse, JsonResponse, EmptyResponse

from datetime import date

from .. import IntegrationTest

class TestComment(IntegrationTest):
    def get_user(self):
        with self.recorder.use_cassette("TestComment.get_user"):
            user = self.moco.User.getlist().items[0]
            return user
    
    def get_customer(self):
        with self.recorder.use_cassette("TestComment.get_customer"):
            customer_create = self.moco.Company.create(
                "TestComment", 
                company_type="customer"
            )

            return customer_create.data

    def get_second_customer(self):
        with self.recorder.use_cassette("TestComment.get_second_customer"):
            customer_create = self.moco.Company.create(
                "TestComment second customer",
                company_type="customer"
            )

            return customer_create.data

    def get_project(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestComment.get_project"):
            project_create = self.moco.Project.create(
                "TestProjects for comments",
                "EUR",
                user.id,
                customer.id,
                finish_date=date(2020, 1, 1)
            )

            return project_create.data

    def test_getlist(self):
        with self.recorder.use_cassette("TestComment.test_getlist"):
            comment_list = self.moco.Comment.getlist()

            assert comment_list.response.status_code == 200
            
            assert isinstance(comment_list, ListingResponse)

    def test_get(self):
        project = self.get_project()
        
        with self.recorder.use_cassette("TestComment.test_get"):
            text = "test create comment"

            comment_create = self.moco.Comment.create(
                project.id, 
                CommentTargetType.PROJECT, 
                text,
            )

            comment_get = self.moco.Comment.get(comment_create.data.id)

            assert comment_create.response.status_code == 200
            assert comment_get.response.status_code == 200
            
            assert isinstance(comment_create, JsonResponse)
            assert isinstance(comment_get, JsonResponse)

            assert comment_get.data.text == text
            assert comment_get.data.commentable_id == project.id
            assert comment_get.data.commentable_type == CommentTargetType.PROJECT
            assert comment_get.data.user.id is not None

    def test_create(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestComment.test_create"):
            text = "test create comment"

            comment_create = self.moco.Comment.create(
                project.id, 
                CommentTargetType.PROJECT, 
                text,
            )

            assert comment_create.response.status_code == 200
            
            assert isinstance(comment_create, JsonResponse)

            assert comment_create.data.text == text
            assert comment_create.data.commentable_id == project.id
            assert comment_create.data.commentable_type == CommentTargetType.PROJECT
            assert comment_create.data.user.id is not None

    def test_create_bulk(self):
        first_customer = self.get_customer()
        second_customer = self.get_second_customer()

        with self.recorder.use_cassette("TestComment.test_create_bulk"):
            text = "bulk comment creation"
            comment_ids = [first_customer.id, second_customer.id]
            comment_type = CommentTargetType.CUSTOMER
            
            comment_create_bulk = self.moco.Comment.create_bulk(
                comment_ids,
                comment_type,
                text,
            )

            assert comment_create_bulk.response.status_code == 200

            assert isinstance(comment_create_bulk, ListingResponse)

            assert len(comment_create_bulk.data) == len(comment_ids)


    def test_update(self):
        project = self.get_project()
        user = self.get_user()


        with self.recorder.use_cassette("TestComment.test_update"):
            update_text = "updated comment"

            comment_create = self.moco.Comment.create(
                project.id,
                CommentTargetType.PROJECT,
                "dummy comment, update comment"
            )

            comment_update = self.moco.Comment.update(
                comment_create.data.id,
                update_text
            )

            assert comment_create.response.status_code == 200
            assert comment_update.response.status_code == 200

            assert isinstance(comment_create, JsonResponse)
            assert isinstance(comment_update, JsonResponse)

            assert comment_update.data.text == update_text
            assert comment_update.data.commentable_id == project.id
            assert comment_update.data.commentable_type == CommentTargetType.PROJECT
            assert comment_update.data.user.id is not None

    def test_delete(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestComment.test_delete"):
            comment_create = self.moco.Comment.create(
                project.id, 
                CommentTargetType.PROJECT, 
                "dummy comment ,test delete"
            )

            comment_delete = self.moco.Comment.delete(comment_create.data.id)

            assert comment_delete.response.status_code == 204

            assert isinstance(comment_delete, EmptyResponse)