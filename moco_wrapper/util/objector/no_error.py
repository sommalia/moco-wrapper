from . import DefaultObjector
from moco_wrapper.util.response import ListingResponse, JsonResponse

class NoErrorObjector(DefaultObjector):
    """
    This class works along the same lines as the DefaultObjector, but it does not convert error responses into actualy exceptions. Instead an ErrorResponse object will be returned.

    .. seealso::

        :class:`moco_wrapper.util.objector.DefaultObjector`

    Example usage:

    .. code-block:: python

        from moco_wrapper.util.objector import NoErrorObjector
        from moco_wrapper import Moco

        no_err_objector = NoErrorObjector()
        m = Moco(
            objector = no_err_objector
        )

    """

    def convert(self, requestor_response):
        """
        converts the data of a response object (for example json) into a python object

        :param requestor_response: response object (see :ref:`response`)
        :returns: modified response object

        .. note:: only :class:`moco_wrapper.util.response.JsonResponse` and :class:`moco_wrapper.util.response.ListingResponse` are object to this conversion.

        .. note:: if the method :meth:`get_class_name_from_request_url` that is used to find the right class for conversion, returns ``None``, no conversion of objects will take place
        """

        if isinstance(requestor_response, JsonResponse) or isinstance(requestor_response, ListingResponse):
            return super(NoErrorObjector, self).convert(requestor_response)
        else:
            return requestor_response