from .base import BaseRequestor

class RawRequestor(BaseRequestor):
    """
    The Raw Requestor is a test requestor that saves all arguments into and object and returns it.

    .. warning::

        Use this requestor only for testing.

    """
    def request(self, method, path, params = None, data = None, **kwargs):
        """
        Request the given ressource

        :param method: HTTP Method (eg. POST, GET, PUT, DELETE)
        :param path: Path of the ressource (e.g. ``/projects``)
        :param params: Url parameters (e.g. ``page=1``, query parameters)
        :param data: Dictionary with data (http body)
        :param kwargs: Additional http arguments.
        :returns: Request objects
        """
        
        return {
            "path": path,
            "data" : data,
            "method": method,
            "params" : params,
            "args": kwargs.items()
        }
