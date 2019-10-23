from .base import MWRAPResponse

class JsonResponse(MWRAPResponse):

    @property 
    def data(self):
        return self.data

    def __init__(self, response):
        super(MWRAPResponse,response).__init()

        self.data = self.json_to_object(response)