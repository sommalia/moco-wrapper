import requests
import time

from .base import BaseRequestor

from ..response import ListingResponse, JsonResponse, ErrorResponse, EmptyResponse, FileResponse

class DefaultRequestor(BaseRequestor):

    def __init__(self):
        self._session = requests.Session()

        self.requests_timestamps = []
        self.error_status_codes = [400, 401, 403, 404, 422, 429]
        self.success_status_codes = [200, 201]

        self.file_response_content_types = ["application/pdf"]


    @property
    def session(self):
        return self._session

    def request(self, path, method, params = None, data = None, **kwargs):


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
                if response.headers["Content-Type"] in self.file_response_content_types:
                    return FileResponse(response)
                else:
                    #json response is the default
                    response_content = response.json()
                    if isinstance(response_content, list):
                        return ListingResponse(response)
                    else:
                        return JsonResponse(response)

            elif response.status_code == 204:
                #no content but success
                return EmptyResponse(response)
            elif response.status_code in self.error_status_codes:
                return ErrorResponse(response)

            print(response)

        except ValueError as ex:
            print(ex)
            response_obj = ErrorResponse(response)

            if response_obj.is_recoverable == True:
                #error is recoverable, try the ressource again
                time.sleep(1)
                return self.request(path, method, params, data, kwargs)
            else:
                return response_obj




    