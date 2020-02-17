from .base import MWRAPResponse

class JsonResponse(MWRAPResponse):
    """
    Class for handling responses where the body can be converted into valid json, but are not listings
    """
    

    @property 
    def data(self):
        """
        Returns the json data of the response as a dictionary
        """
        return self._data

    def __init__(self, response):
        """
        class constructor

        :param response: response object
        """
        super(JsonResponse, self).__init__(response)

        self._data = self.response.json()

    def __str__(self):
        return "<JsonResponse, Status Code: {}, Data: {}>".format(self.response.status_code, self.response.text)