import pytest

from moco_wrapper.models.comment import CommentTargetType
from .. import UnitTest

class TestComment(UnitTest):
    def test_create(self):
        commentable_type = "Offer"
        commentable_id = 123
        text = "this is the comment text"

        response = self.moco.Comment.create(commentable_id, commentable_type, text)
        data = response["data"]

        assert data["commentable_id"] == commentable_id
        assert data["commentable_type"] == CommentTargetType.OFFER
        assert data["text"] == text

        assert response["method"] == "POST"

    def test_create_bulk(self):
        commentable_type = "Offer"
        commentable_ids = [123, 124, 125]
        text = "this is the comment text"

        response = self.moco.Comment.create_bulk(commentable_ids, commentable_type, text)
        data = response["data"]

        assert data["commentable_ids"] == commentable_ids
        assert data["commentable_type"] == CommentTargetType.OFFER
        assert data["text"] == text

        assert response["method"] == "POST"

    def test_getlist(self):
        commentable_type = "Customer"
        commentable_id = 4
        user_id = 4
        manual = False

        response = self.moco.Comment.getlist(commentable_type=commentable_type, commentable_id=commentable_id, user_id=user_id, manual=manual)

        params = response["params"]

        assert params["commentable_id"] == commentable_id
        assert params["commentable_type"] == CommentTargetType.CUSTOMER
        assert params["user_id"] == user_id
        assert params["manual"] == manual

        assert response["method"] == "GET"

    def test_getlist_sort_default(self):
        sort_by = "sort field"

        response = self.moco.Comment.getlist(sort_by=sort_by)
        params = response["params"]

        assert params["sort_by"] == "{} asc".format(sort_by)
        
    def test_getlist_sort_overwrite(self):
        sort_by = "sort field"
        sort_order = "desc"

        response = self.moco.Comment.getlist(sort_by=sort_by, sort_order=sort_order)
        params = response["params"]

        assert params["sort_by"] == "{} {}".format(sort_by, sort_order)

    def test_getlist_page_default(self):
        default_page = 1

        response = self.moco.Comment.getlist()
        params = response["params"]

        assert params["page"] == default_page

    def test_getlist_page_overwrite(self):
        overwrite_page = 22

        response = self.moco.Comment.getlist(page=overwrite_page)
        params = response["params"]

        assert params["page"] == overwrite_page

    def test_get(self):
        comment_id = 5

        response = self.moco.Comment.get(comment_id)

        assert response["method"] == "GET"

    def test_delete(self):
        comment_id = 5

        response = self.moco.Comment.delete(comment_id)

        assert response["method"] == "DELETE"

    def test_update(self):
        comment_id = 65
        text = "updated text"
        commentable_id = 1234
        commentable_type = "Project"

        response = self.moco.Comment.update(comment_id, text=text, commentable_id=commentable_id, 
        commentable_type=commentable_type)

        data = response["data"]

        assert data["text"] == text
        assert data["commentable_id"] == commentable_id
        assert data["commentable_type"] == commentable_type

        assert response["method"] == "PUT"
