import requests
import time
import collections

from moco_wrapper.util.requestor.base import BaseRequestor
from moco_wrapper.util.response import PagedListResponse, ListResponse, ObjectResponse, ErrorResponse, EmptyResponse, \
    FileResponse


class NoRetryRequestor(BaseRequestor):
    """
    This requestor works along the same lines as the :class:`moco_wrapper.util.requestor.DefaultRequestor`, but when this requestor comes along the http code 429 for too many requests it just returns an error response.

    Use this requestor if you write integration tests or dont have time for retrying the resource.

    Example usage:

    .. code-block:: python

        from moco_wrapper.util.requestor import NoRetryRequestor
        from moco_wrapper import Moco

        no_retry = NoRetryRequestor()
        m = Moco(
            requestor = no_retry
        )

    .. seealso::

        :class:`moco_wrapper.util.requestor.DefaultRequestor`
    """

    def __init__(self):
        """
        Class constructor
        """
        self._session = requests.Session()

    @property
    def session(self):
        """
        Http Session this requestor uses
        """
        return self._session

    def request(self, method, path, params=None, data=None, **kwargs):
        """
        Request the given resource

        :param method: HTTP Method (eg. POST, GET, PUT, DELETE)
        :param path: Path of the resource (e.g. ``/projects``)
        :param params: Url parameters (e.g. ``page=1``, query parameters)
        :param data: Dictionary with data (http body)
        :param kwargs: Additional http arguments.

        :type method: str
        :type path: str
        :type params: dict
        :type data: dict

        :returns: Response object
        """

        if params is not None:
            params = self._format_params(params)

        # format data submitted to requests as json
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
                # filter by content type what type of response this is
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
                        return ListResponse(response) # response is an unpaged list

                # return single json response
                return ObjectResponse(response)

            # check if the response has an error status code
            if response.status_code in self.ERROR_STATUS_CODES:
                error_response = ErrorResponse(response)
                return error_response

        except ValueError as ex:
            # print("ValueError in response conversion:" + str(ex))
            response_obj = ErrorResponse(response)
            return response_obj
