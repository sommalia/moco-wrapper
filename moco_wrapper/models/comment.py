from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH

from enum import Enum

class CommentTargetType(str, Enum):
    """
    Enumeration for allowed values used that can be supplied for the ``commentable_type`` argument in :meth:`.Comment.create`, :meth:`.Comment.create_bulk` and :meth:`.Comment.getlist`

    .. code-block:: python
    
        from moco_wrapper import Moco
        from moco_wrapper.models.comment import CommentTargetType

        m = Moco()
        comment_create = m.Comment.create(
            ..
            commentable_type = CommentTargetType.DEAL
        )

    """
    USER = "User"
    DEAL = "Deal"
    OFFER = "Offer"
    OFFERCONFIRMATION = "OfferConfirmation"
    CUSTOMER = "Customer"
    PROJECT = "Project"
    INVOICE = "Invoice"
    CONTACT = "Contact"

class Comment(MWRAPBase):
    """
    Class for handling comments.

    Comments can be created for a multitude of objects. So when creating comments one must specify which type of object they mean (see :class:`.CommentTargetType`)
    
    Example Usage:

    .. code-block:: python
    
    
        m = Moco()
        project_id = 22
        comment_create = m.Comment.create(
            project_id, #id of the thing we comment
            "PROJECT", #object type
            "example comment text"
        )
    """

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def create(
        self,
        commentable_id: int,
        commentable_type: CommentTargetType,
        text: str
        ):
        """
        Create a single comment. 

        :param commentable_id: Id of the object to create the comment of (i.e the project id of the project we want to comment on)
        :param commentable_type: Type of object to create the comment for.
        :param text: Comment text

        :type commentable_id: int
        :type commentable_type: :class:`.CommentTargetType`, str
        :type text: str

        :returns: The created comment
        """
        data = {
            "commentable_id": commentable_id,
            "commentable_type" : commentable_type,
            "text": text
        }

        return self._moco.post(API_PATH["comment_create"], data=data)

    def create_bulk(
        self,
        commentable_ids: list,
        commentable_type: CommentTargetType,
        text: str
        ):
        """
        Create a comment for multiple target objects.

        :param commentable_ids: ids of the objects we want to comment under ie. [123, 124, 125]
        :param commentable_type: type of object to create the comment for. For allowed values see :class:`.CommentTargetType`.
        :param text: comment text

        :type commentable_ids: list
        :type commentable_type: :class:`.CommentTargetType`, str
        :type text: str

        :returns: List of created comments.
        """
        data = {
            "commentable_ids" : commentable_ids,
            "commentable_type": commentable_type,
            "text" : text
        }

        return self._moco.post(API_PATH["comment_create_bulk"], data=data)

    def update(
        self,
        comment_id: int,
        text: str
        ):
        """
        Update a comment.

        :param comment_id: The id of the comment to update
        :param text: Comment text

        :type comment_id: int
        :type text: str

        :returns: The created comment
        """
        data = {
            "text" : text,  
        }

        return self._moco.put(API_PATH["comment_update"].format(id=comment_id), data=data)

    def delete(
        self,
        comment_id: int,
        ):
        """
        Delete a comment.

        :param comment_id: Id of the comment to delete

        :type comment_id: int

        :returns: Empty response on success
        """

        return self._moco.delete(API_PATH["comment_delete"].format(id=comment_id))

    def get(
        self,
        comment_id: int
        ):
        """
        Retrieve a single comment.

        :param comment_id: Id of the comment

        :type comment_id: int

        :returns: Single comment
        """
        return self._moco.get(API_PATH["comment_get"].format(id=comment_id))

    def getlist(
        self,
        commentable_type: CommentTargetType = None,
        commentable_id: int = None,
        user_id: int = None,
        manual: bool = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
        ):
        """
        Retrieve a list of comments.

        :param commentable_type: Type of object the comment(s) belong to
        :param commentable_id: Id of the object the comment belongs to
        :param user_id: User id of the creator
        :param manual: If the comment was user-created of generated
        :param sort_by: Field to sort the results by
        :param sort_order: asc or desc
        :param page: Page number (default 1)

        :type commentable_type: :class:`.CommentTargetType`, str
        :type commentable_id: int
        :type user_id: int
        :type manual: bool
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: list of comments
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
