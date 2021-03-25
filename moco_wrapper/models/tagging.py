from typing import List

from moco_wrapper.util.endpoint import Endpoint
from moco_wrapper.models import objector_models as om
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

    @staticmethod
    def endpoints() -> List[Endpoint]:
        """
        Returns all endpoints associated with the model

        :returns: List of Endpoint objects
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`

        """
        return [
            Endpoint("tagging_add", "/taggings/{entity}/{entity_id}", "PATCH"),
            Endpoint("tagging_replace", "/taggings/{entity}/{entity_id}", "PUT"),
            Endpoint("tagging_get", "/taggings/{entity}/{entity_id}", "GET"),
            Endpoint("tagging_delete", "/taggings/{entity}/{entity_id}", "DELETE")
        ]

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def get(
        self,
        entity: TaggingEntity,
        entity_id: int
    ):
        """
        Get the tags associated with an entity

        :param entity: Type of entity to add tags to
        :param entity_id: Id of the entity

        :type entity: TaggingEntity, str
        :type entity_id: int

        :returns: List of tags assigned to the entity
        :rtype: :class:`moco_wrapper.util.response.ListResponse`
        """
        ep_params = {
            "entity": entity,
            "entity_id": entity_id
        }

        return self._moco.get("tagging_get", ep_params=ep_params)

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

        :returns: List of tags assigned to the entity
        :rtype: :class:`moco_wrapper.util.response.ListResponse`

        .. note::

           If you supply tags that already exist for the entity they will be ignored.
        """
        ep_params = {
            "entity": entity,
            "entity_id": entity_id
        }

        data = {
            "tags": tags
        }

        return self._moco.patch("tagging_add", ep_params=ep_params, data=data)

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

        :returns: List of tags assigned to the entity
        :rtype: :class:`moco_wrapper.util.response.ListResponse`

        .. note::

            You can remove all tags from an entity by supplying an empty list.
        """
        ep_params = {
            "entity": entity,
            "entity_id": entity_id
        }

        data = {
            "tags": tags
        }

        return self._moco.put("tagging_replace", ep_params=ep_params, data=data)

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

        :returns: List of tags assigned to the entity
        :rtype: :class:`moco_wrapper.util.response.ListResponse`
        """
        ep_params = {
            "entity": entity,
            "entity_id": entity_id
        }

        data = {
            "tags": tags
        }

        return self._moco.delete("tagging_delete", ep_params=ep_params, data=data)
