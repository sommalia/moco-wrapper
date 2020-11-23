from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH
from enum import Enum


class TaggingEntity(str, Enum):
    """
    Enumeration for all available entity types that can be supplied for the ``entity`` argument of :meth:`.Tagging.add`,
    :meth:`.Tagging.replace` and :meth:`.Tagging.delete`.

    Example Usage:

    .. code-block:: python

        from moco_wrapper import Moco
        from moco_wrapper.models.tagging import TaggingEntity

        m = Moco()

        project_id = 22
        tags_add = m.Tagging.add(
            entity = TaggingEntity.PROJECT,
            entity_id = project_id,
            tags = [ "these", "are", "the", "tags" ]
        )
    """
    COMPANY = "Company"
    CONTACT = "Contact"
    PROJECT = "Project"
    DEAL = "Deal"
    PURCHASE = "Invoice"
    OFFER = "Offer"


class Tagging(MWRAPBase):
    """
    Class for handling tags/labels.
    """

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def add(
        self,
        entity: TaggingEntity,
        entity_id: int,
        tags: list
    ):
        """
        Add tags to an entity.

        :param entity: Type of entity to add tags to
        :param entity_id: Id of the entity
        :param tags: List of tags to add

        :type entity: TaggingEntity, str
        :type entity_id: int
        :type tags: list

        .. note::

           If you supply tags that already exist for the entity they will be ignored.
        """

        data = {
            "tags": tags
        }

        return self._moco.patch(
            API_PATH["tagging_add"].format(entity=entity, entity_id=entity_id),
            data=data
        )

    def replace(
        self,
        entity: TaggingEntity,
        entity_id: int,
        tags: list
    ):
        """
        Replace the tags of an entity.

        :param entity: Type of entity to replace tags for
        :param entity_id: Id of the entity
        :param tags: New list of tags for the entity

        :type entity: TaggingEntity, str
        :type entity_id: int
        :type tags: list

        .. note::

            You can remove all tags from an entity by supplying an empty list.
        """

        data = {
            "tags": tags
        }

        return self._moco.put(
            API_PATH["tagging_replace"].format(entity=entity, entity_id=entity_id),
            data=data
        )

    def delete(
        self,
        entity: TaggingEntity,
        entity_id: int,
        tags: list
    ):
        """
        Removes supplied tags from an entity

        :param entity: Type of entity to remove tags for
        :param entity_id: Id of the entity
        :param tags: List of tags to remove

        :type entity: TaggingEntity, str
        :type entity_id: int
        :type tags: list
        """

        data = {
            "tags": tags
        }

        return self._moco.delete(
            API_PATH["tagging_delete"].format(entity=entity, entity_id=entity_id),
            data=data
        )
