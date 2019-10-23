from .base import MWRAPResponse

class JsonResponse(MWRAPResponse):

    @property 
    def data(self):
        return self._data

    def __init__(self, response):
        super(JsonResponse, self).__init__(response)

        self._data = self.json_to_object(response.text)