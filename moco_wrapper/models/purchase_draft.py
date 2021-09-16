from typing import List

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.util.endpoint import Endpoint
from moco_wrapper.models import objector_models as om


class PurchaseDraft(MWRAPBase):
    """
    Class for handling purchase drafts
    """

    @staticmethod
    def endpoints() -> List[Endpoint]:
        """
        Returns all endpoints associated with the model

        :returns: List of Endpoint objects
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`

        """
        return [
            Endpoint("purchase_draft_getlist", "/purchases/drafts", "GET", om.PurchaseDraft),
            Endpoint("purchase_draft_get", "/purchases/drafts/{id}", "GET", om.PurchaseDraft),
            Endpoint("purchase_draft_pdf", "/purchases/drafts/{id}.pdf", "GET")
        ]

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def getlist(self):
        """
        Retrieve a list of purchase drafts

        :returns: List of purchase drafts
        :rtype: :class:`moco_wrapper.util.response.ListResponse`
        """
        return self._moco.get("purchase_draft_getlist")

    def get(
        self,
        draft_id: int
    ):
        """
        Retrieve a single purchase draft

        :param draft_id: Id of the draft to retrieve

        :type draft_id: int

        :returns: Single Purchase draft
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "id": draft_id
        }

        return self._moco.get("purchase_draft_get", ep_params=ep_params)

    def pdf(
        self,
        draft_id: int
    ):
        """
        Retrieve a draft document

        :param draft_id: Id of the draft to retrieve the document for

        :type draft_id: int

        :returns: The draft document
        :rtype: :class:`moco_wrapper.util.response.FileResponse`
        """
        ep_params = {
            "id": draft_id
        }
        return self._moco.get("purchase_draft_pdf", ep_params=ep_params)
