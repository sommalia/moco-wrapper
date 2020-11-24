from moco_wrapper.models.comment import CommentTargetType
from moco_wrapper.models.company import CompanyType
from moco_wrapper.util.response import ObjectResponse, ListResponse, PagedListResponse, EmptyResponse


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
                name="TestComment.get_customer",
                company_type=CompanyType.CUSTOMER
            )

            return customer_create.data

    def get_other_customer(self):
        with self.recorder.use_cassette("TestComment.get_other_customer"):
            customer_create = self.moco.Company.create(
                name="TestComment.get_other_customer",
                company_type=CompanyType.CUSTOMER
            )

            return customer_create.data

    def get_project(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestComment.get_project"):
            project_create = self.moco.Project.create(
                name="TestComment.get_project",
                currency="EUR",
                leader_id=user.id,
                customer_id=customer.id,
                finish_date=date(2020, 1, 1)
            )

            return project_create.data

    def test_getlist(self):
        with self.recorder.use_cassette("TestComment.test_getlist"):
            comment_list = self.moco.Comment.getlist()

            assert comment_list.response.status_code == 200

            assert isinstance(comment_list, PagedListResponse)

            assert comment_list.current_page == 1
            assert comment_list.is_last is not None
            assert comment_list.next_page is not None
            assert comment_list.total is not None
            assert comment_list.page_size is not None

    def test_get(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestComment.test_get"):
            text = "TestComment.test_get_create"

            comment_create = self.moco.Comment.create(
                commentable_id=project.id,
                commentable_type=CommentTargetType.PROJECT,
                text=text,
            )

            comment_get = self.moco.Comment.get(
                comment_id=comment_create.data.id
            )

            assert comment_create.response.status_code == 200
            assert comment_get.response.status_code == 200

            assert isinstance(comment_create, ObjectResponse)
            assert isinstance(comment_get, ObjectResponse)

            assert comment_get.data.text == text
            assert comment_get.data.commentable_id == project.id
            assert comment_get.data.commentable_type == CommentTargetType.PROJECT
            assert comment_get.data.user.id is not None

    def test_create(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestComment.test_create"):
            text = "TestComment.test_create"

            comment_create = self.moco.Comment.create(
                commentable_id=project.id,
                commentable_type=CommentTargetType.PROJECT,
                text=text,
            )

            assert comment_create.response.status_code == 200

            assert isinstance(comment_create, ObjectResponse)

            assert comment_create.data.text == text
            assert comment_create.data.commentable_id == project.id
            assert comment_create.data.commentable_type == CommentTargetType.PROJECT
            assert comment_create.data.user.id is not None

    def test_create_bulk(self):
        customer = self.get_customer()
        other_customer = self.get_other_customer()

        with self.recorder.use_cassette("TestComment.test_create_bulk"):
            text = "TestComment.test_create_bulk"
            comment_ids = [customer.id, other_customer.id]
            comment_type = CommentTargetType.CUSTOMER

            comment_create_bulk = self.moco.Comment.create_bulk(
                commentable_ids=comment_ids,
                commentable_type=comment_type,
                text=text,
            )

            assert comment_create_bulk.response.status_code == 200

            assert isinstance(comment_create_bulk, ListResponse)

            assert len(comment_create_bulk.data) == len(comment_ids)

    def test_update(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestComment.test_update"):
            update_text = "TestComment.test_update"

            comment_create = self.moco.Comment.create(
                commentable_id=project.id,
                commentable_type=CommentTargetType.PROJECT,
                text="TestComment.test_update_create"
            )

            comment_update = self.moco.Comment.update(
                comment_id=comment_create.data.id,
                text=update_text
            )

            assert comment_create.response.status_code == 200
            assert comment_update.response.status_code == 200

            assert isinstance(comment_create, ObjectResponse)
            assert isinstance(comment_update, ObjectResponse)

            assert comment_update.data.text == update_text
            assert comment_update.data.commentable_id == project.id
            assert comment_update.data.commentable_type == CommentTargetType.PROJECT
            assert comment_update.data.user.id is not None

    def test_delete(self):
        project = self.get_project()

        with self.recorder.use_cassette("TestComment.test_delete"):
            comment_create = self.moco.Comment.create(
                commentable_id=project.id,
                commentable_type=CommentTargetType.PROJECT,
                text="TestActivity.test_delete_create"
            )

            comment_delete = self.moco.Comment.delete(
                comment_id=comment_create.data.id
            )

            assert comment_delete.response.status_code == 204

            assert isinstance(comment_delete, EmptyResponse)
