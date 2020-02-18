import requests
import time
import collections

from .base import BaseRequestor

from ..response import ListingResponse, JsonResponse, ErrorResponse, EmptyResponse, FileResponse

class NoRetryRequestor(BaseRequestor):
    """
    Same as the DefaultRequestor, but does not retry any reconverable errors
    """
    def __init__(self):
        self._session = requests.Session()

        self.requests_timestamps = []
        self.error_status_codes = [400, 401, 403, 404, 422, 429]
        self.success_status_codes = [200, 201, 204]

        self.file_response_content_types = ["application/pdf"]

    @property
    def session(self):
        return self._session

    def request(self, path, method, params = None, data = None, **kwargs):
        #if the request is beeing retried wait for a bit to not trigger 429 error responses

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

            if response.status_code in self.success_status_codes:
                #filter by content type what type of response this is 
                if response.status_code == 204:
                    #no content but success
                    return EmptyResponse(response)
                elif response.status_code == 200 and response.text.strip() == "":
                    #touch endpoint returns 200 with no content
                    return EmptyResponse(response)
                else:
                    if response.headers["Content-Type"] in self.file_response_content_types:
                        return FileResponse(response)
                    else:
                        #print(response.content)
                        #json response is the default
                        response_content = response.json()
                        if isinstance(response_content, list):
                            return ListingResponse(response)
                        else:
                            return JsonResponse(response)

            elif response.status_code in self.error_status_codes:
                error_response = ErrorResponse(response)
                return error_response

        except ValueError as ex:

            print("ValueError in response conversion:" + str(ex))
            response_obj = ErrorResponse(response)
            return response_obj