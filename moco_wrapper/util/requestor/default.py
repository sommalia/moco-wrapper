import requests
import time

from moco_wrapper.util.requestor.base import BaseRequestor
from moco_wrapper.util.response import PagedListResponse, ListResponse, ObjectResponse, ErrorResponse, EmptyResponse, FileResponse


class DefaultRequestor(BaseRequestor):
    """
    Default Requestor class that is used by the :class:`moco_wrapper.Moco` instance.

    When the default requestor requests a resources and it sees the error code 429 (too many requests),
    it waits a bit and then tries the request again. If you do not want that behaviour, use
    :class:`moco_wrapper.util.requestor.NoRetryRequestor`.

    .. seealso::
        :class:`moco_wrapper.util.requestor.NoRetryRequestor`
    """

    def __init__(
        self,
        delay_ms: float = 1000.0
    ):
        """
        Class constructor

        :param delay_ms: How long the requestor should wait before retrying the resource again (default 1000).

        Overwrite delay:

        .. code-block:: python

            from moco_wrapper.util.requestor import DefaultRequestor
            from moco_wrapper import Moco

            #wait 5 seconds on an error
            lazy_requestor = DefaultRequestor(
                delay_ms = 5000
            )

            m = Moco(
                requestor = lazy_requestor
            )
        """
        self._session = requests.Session()

        self.delay_milliseconds_on_error = delay_ms

    @property
    def session(self):
        """
        Http Session this requestor uses
        """
        return self._session

    def request(
        self,
        method: str,
        path: str,
        params: dict = None,
        data: dict = None,
        delay_ms: float = 0,
        **kwargs
    ):
        """
        Request the given resource.

        :param method: HTTP Method (eg. POST, GET, PUT, DELETE)
        :param path: Path of the resource (e.g. ``/projects``)
        :param params: Url parameters (e.g. ``page=1``, query parameters) (default ``None``)
        :param data: Dictionary with data (http body) (default ``None``)
        :param delay_ms: Delay in milliseconds the requestor should wait before sending the request
            (used for retrying, default ``0``)
        :param kwargs: Additional http arguments.

        :type method: str
        :type path: str
        :type params: dict
        :type data: dict
        :type delay_ms: float

        :returns: Response object
        """
        # if the request is being retried wait for a bit to not trigger 429 error responses
        if delay_ms > 0:
            time.sleep(delay_ms / 1000.0)

        if params is not None:
            params = self._format_params(params)

        response = None
        if method == "GET":
            response = self.session.get(path, params=params, json=data, **kwargs)
        elif method == "POST":
            response = self.session.post(path, params=params, json=data, **kwargs)
        elif method == "DELETE":
            response = self.session.delete(path, params=params, json=data, **kwargs)
        elif method == "PUT":
            response = self.session.put(path, params=params, json=data, **kwargs)
        elif method == "PATCH":
            response = self.session.patch(path, params=params, json=data, **kwargs)

        # convert the response into an MWRAPResponse object
        try:
            # check if the response has a success status code
            if response.status_code in self.SUCCESS_STATUS_CODES:
                if response.status_code == 204:
                    # no content but success
                    return EmptyResponse(response)

                if response.status_code == 200 and response.text.strip() == "":
                    # touch endpoint returns 200 with no content
                    return EmptyResponse(response)

                if response.headers["Content-Type"] == "application/pdf":
                    return FileResponse(response)

                # json response handling is the default
                response_content = response.json()

                # if response is a list, return list response
                if isinstance(response_content, list):
                    if "X-Page" in response.headers.keys():
                        return PagedListResponse(response)  # response is a paged list
                    else:
                        return ListResponse(response)  # response is an unpdaged list

                # return object response as default
                return ObjectResponse(response)

            # check if the response has an error status code
            if response.status_code in self.ERROR_STATUS_CODES:
                response_obj = ErrorResponse(response)

                if response_obj.is_recoverable:
                    return self.request(method, path, params=params, data=data,
                                        delay_ms=self.delay_milliseconds_on_error, **kwargs)

                # error is not recoverable
                return response_obj

        except ValueError as ex:
            response_obj = ErrorResponse(response)
            if response_obj.is_recoverable:
                # error is recoverable, try the resource again
                return self.request(method, path, params=params, data=data,
                                    delay_ms=self.delay_milliseconds_on_error, **kwargs)

            # error is not recoverable
            return response_obj
