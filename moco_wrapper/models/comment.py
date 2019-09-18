from .base import MocoBase
from ..const import API_PATH

class Comment(MocoBase):
    """Class for handling comments."""

    def __init__(self, moco):
        self._moco = moco

    def create(
        self,
        commentable_id,
        commentable_type,
        text
        ):
        """create a comment 

        :param commentable_id: id of the object to create the comment of (i.e the project id of the project we want to comment on)
        :param commentable_type: type of object to create the comment of (i.e when we want to comment on a project this is "project"), available values are  "User", "Deal", "Offer", "OfferConfirmation", "Customer", "Project", "Invoice", "Contact"
        :param text: comment text
        :returns: the created comment
        """
        data = {
            "commentable_id": commentable_id,
            "commentable_type" : commentable_type,
            "text": text
        }

        return self._moco.post(API_PATH["comment_create"], data=data)

    def create_bulk(
        self,
        commentable_ids,
        commentable_type,
        text
        ):
        """create a comment under multplie objects of the same type
        :param commentable_ids: ids of the objects we want to comment under ie. [123, 124, 125]
        :param commentable_type: type of object to create the comment of (i.e when we want to comment on a project this is "project"), available values are  "User", "Deal", "Offer", "OfferConfirmation", "Customer", "Project", "Invoice", "Contact"
        :param text: comment text
        """
        data = {
            "commentable_ids" : commentable_ids,
            "commentable_type": commentable_type,
            "text" : text
        }

        return self._moco.post(API_PATH["comment_create_bulk"], data=data)

    def update(
        self,
        id,
        commentable_id = None,
        commentable_type = None,
        text = None
        ):
        """update a comment

        :param id: the id of the comment to update
        :param commentable_id: id of the object to create the comment of (i.e the project id of the project we want to comment on)
        :param commentable_type: type of object to create the comment of (i.e when we want to comment on a project this is "project"), available values are  "User", "Deal", "Offer", "OfferConfirmation", "Customer", "Project", "Invoice", "Contact"
        :param text: comment text
        :returns: the created comment
        """
        data = {}
        for key, value in (
            ("commentable_id", commentable_id),
            ("commentable_type", commentable_type),
            ("text", text)
        ):
            if value is not None:
                data[key] = value

        return self._moco.put(API_PATH["comment_update"].format(id=id), data=data)

    def delete(
        self,
        id
        ):
        """delete a comment

        :param id: id of the comment to delete
        """

        return self._moco.delete(API_PATH["comment_delete"].format(id=id))

    def get(
        self,
        id
        ):
        """retrieve a single comment

        :param id: id of the comment
        :returns: a single comment object
        """
        return self._moco.get(API_PATH["comment_get"].format(id=id))

    def getlist(
        self,
        commentable_type = None,
        commentable_id = None,
        user_id = None,
        manual = None,
        sort_by = None,
        sort_order = 'asc',
        page = 1
        ):
        """retrieve a list of comments

        :param commentable_type: type of object the comment(s) belong to available values are  "User", "Deal", "Offer", "OfferConfirmation", "Customer", "Project", "Invoice", "Contact"
        :param commentable_id: id of the object the comment belongs to
        :param user_id: user id of the creator
        :param manual: true/false user-created of generated
        :param sort_by: field to sort the results by
        :param sort_order: asc or desc
        :param page: page number (default 1)
        :returns: list of comemnt objects
        """
        params = {}
        for key, value in (
            ("commentable_type", commentable_type),
            ("commentable_id", commentable_id),
            ("user_id", user_id),
            ("manual", manual),
            ("page", page)
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["comment_getlist"], params=params)


        