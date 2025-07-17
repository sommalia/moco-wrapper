from typing import List

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.util.endpoint import Endpoint
from moco_wrapper.models import objector_models as om


class Webhook(MWRAPBase):
    """
    Class for handling authentication against the moco api with a users email address and password.

    This model is used internally when the moco instance is created with no api key in the authentication object and
    will be invoked before the first request is fired.
    """

    @staticmethod
    def endpoints() -> List[Endpoint]:
        """
        Returns all endpoints associated with the model

        :returns: List of Endpoint objects
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`

        """
        return [
            Endpoint("webhook_create", "/account/web_hooks", "POST", om.Webhook),
            Endpoint("webhook_update", "/account/web_hooks/{id}", "PUT", om.Webhook),
            Endpoint("webhook_delete", "/account/web_hooks/{id}", "DELETE"),
            Endpoint("webhook_get", "/account/web_hooks/{id}", "GET", om.Webhook),
            Endpoint("webhook_getlist", "/account/web_hooks", "GET", om.Webhook),
            Endpoint("webhook_disable", "/account/web_hooks/{id}/disable", "PUT", om.Webhook),
            Endpoint("webhook_enable", "/account/web_hooks/{id}/enable", "PUT", om.Webhook),
        ]

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def create(
        self,
        target: str,
        event: str,
        hook: str,
    ):
        """
        Creates a new Webhook.

        :param target: The moco Target of the webhook
        :param event: The event on the target (create, update, delete)
        :param hook: The URL to send the webhook to

        :type target: str
        :type event: str
        :type hook: str

        :returns: The created webhook object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """

        data = {
            "target": target,
            "event": event,
            "hook": hook,
        }

        return self._moco.post("webhook_create", data=data)

    def update(
        self,
        webhook_id,
        target: str,
        event: str,
        hook: str,
    ):
        """
        Updates an existing webhook.

        :param webhook_id: Id of the webhook to delete
        :param target: The moco Target of the webhook
        :param event: The event on the target (create, update, delete)
        :param hook: The URL to send the webhook to

        :type webhook_id: int
        :type target: str
        :type event: str
        :type hook: str

        :returns: The updated webhook object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """

        ep_params = {"id": webhook_id}

        data = {}
        for key, value in (
            ("target", target),
            ("event", event),
            ("hook", hook),
        ):
            if value is not None:
                data[key] = value

        return self._moco.put("webhook_update", ep_params=ep_params, data=data)

    def delete(self, webhook_id: int):
        """
        Deletes an existing webhook.

        :param webhook_id: Id of the webhook to delete

        :type webhook_id: int

        :returns: Empty response on success
        :rtype: :class:`moco_wrapper.util.response.EmptyResponse`
        """
        ep_params = {"id": webhook_id}

        return self._moco.delete("webhook_delete", ep_params=ep_params)

    def get(self, webhook_id: int):
        """
        Get a single webhook.

        :param webhook_id: Id of the webhook to delete

        :type webhook_id: int

        :returns: Single webhook object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {"id": webhook_id}

        return self._moco.get("webhook_get", ep_params=ep_params)

    def getlist(self, include_archived: bool = None, sort_by: str = None, sort_order: str = "asc", page: int = 1):
        """
        Get a list of webhooks.

        :param sort_by: Sort by key (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of Webhooks
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`
        """

        params = {}
        for key, value in (
            ("include_archived", include_archived),
            ("page", page),
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get("webhook_getlist", params=params)

    def disable(self, webhook_id: int):
        """
        disables an existing webhook.

        :param webhook_id: Id of the webhook to disable

        :type webhook_id: int

        :returns: Empty response on success
        :rtype: :class:`moco_wrapper.util.response.EmptyResponse`
        """
        ep_params = {"id": webhook_id}

        return self._moco.put("webhook_disable", ep_params=ep_params)

    def enable(self, webhook_id: int):
        """
        enables an existing webhook.

        :param webhook_id: Id of the webhook to enable

        :type webhook_id: int

        :returns: Empty response on success
        :rtype: :class:`moco_wrapper.util.response.EmptyResponse`
        """
        ep_params = {"id": webhook_id}

        return self._moco.put("webhook_enable", ep_params=ep_params)
