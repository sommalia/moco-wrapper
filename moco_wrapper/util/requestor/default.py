import requests
import time

from .base import BaseRequestor

from ..response import ListingReponse, JsonResponse, ErrorResponse

class DefaultRequestor(BaseRequestor):

    def __init__(self):
        self._session = requests.Session()

        self.requests_timestamps = []

    @property
    def session(self):
        return self._session

    def request(self, path, method, params = None, data = None, **kwargs):

        time.sleep(1)

        response = None
        if method == "GET":
            response =  self.session.get(path, params=params, data=data, **kwargs)
        elif method == "POST":
            response = self.session.post(path, params=params, data=data, **kwargs)
        elif method == "DELETE":
            response = self.session.post(path, params=params, data=data, **kwargs)
        elif method == "PUT":
            response = self.session.put(path, params=params, data=data, **kwargs)
        elif method == "PATCH":
            response = self.session.patch(path, params=params, data=data, **kwargs)

        #convert the reponse into an MWRAPResponse object
        try:
            response_content = response.json()
            if isinstance(response_content, list):
                return ListingResponse(response)
            else:
                return JsonResponse(response)
        except ValueError:
            response_obj = ErrorResponse(response)

            if response_obj.is_recoverable == True:
                #error is recoverable, try the ressource again
                return self.request(path, method, params, data, kwargs)
            else:
                return response_obj




    