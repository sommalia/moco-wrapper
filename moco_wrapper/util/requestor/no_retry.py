import requests
import time
import collections

from moco_wrapper.util.requestor.base import BaseRequestor
from moco_wrapper.util.response import ListingResponse, JsonResponse, ErrorResponse, EmptyResponse, FileResponse

class NoRetryRequestor(BaseRequestor):
    """
    This requestor works along the same lines as the :class:`moco_wrapper.util.requestor.DefaultRequestor`, but when this requestor comes along the http code 429 for too many requests it just returns an error response.

    Use this requestor if you write integration tests or dont have time for retrying the ressource.

    Example usage:

    .. code-block:: python

        from moco_wrapper.util.requestr import NoRetryRequestor
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

    def request(self, method, path, params = None, data = None, **kwargs):
        """
        Request the given ressource

        :param method: HTTP Method (eg. POST, GET, PUT, DELETE)
        :param path: Path of the ressource (e.g. ``/projects``)
        :param params: Url parameters (e.g. ``page=1``, query parameters)
        :param data: Dictionary with data (http body)
        :param kwargs: Additional http arguments.
        :returns: Response object
        """

        #format data submitted to requests as json
        response = None
        if method == "GET":
            response =  self.session.get(path, params=params, json=data, **kwargs)
        elif method == "POST":
            response = self.session.post(path, params=params, json=data, **kwargs)
        elif method == "DELETE":
            response = self.session.delete(path, params=params, json=data, **kwargs)
        elif method == "PUT":
            response = self.session.put(path, params=params, json=data, **kwargs)
        elif method == "PATCH":
            response = self.session.patch(path, params=params, json=data, **kwargs)

        #convert the reponse into an MWRAPResponse object
        try:

            if response.status_code in self.SUCCESS_STATUS_CODES:
                #filter by content type what type of response this is 
                if response.status_code == 204:
                    #no content but success
                    return EmptyResponse(response)
                elif response.status_code == 200 and response.text.strip() == "":
                    #touch endpoint returns 200 with no content
                    return EmptyResponse(response)
                else:
                    if response.headers["Content-Type"] == "application/pdf":
                        return FileResponse(response)
                    else:
                        #print(response.content)
                        #json response is the default
                        response_content = response.json()
                        if isinstance(response_content, list):
                            return ListingResponse(response)
                        else:
                            return JsonResponse(response)
            elif response.status_code in self.ERROR_STATUS_CODES:
                error_response = ErrorResponse(response)
                return error_response

        except ValueError as ex:
            print("ValueError in response conversion:" + str(ex))
            response_obj = ErrorResponse(response)
            return response_obj