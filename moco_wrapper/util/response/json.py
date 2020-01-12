from .base import MWRAPResponse

class JsonResponse(MWRAPResponse):
    """
    Class for handling responses where the body can be converted into valid json, but are not listings
    """

    @property 
    def data(self):
        """
        Returns the json data of the response as an object
        """
        return self._data

    def __init__(self, response):
        """
        class constructor

        :param response: response object
        """
        super(JsonResponse, self).__init__(response)

        self._data = self.json_to_object(response.text)

    def __str__(self):
        return "<JsonResponse, Status Code: {}, Data: {}>".format(self.response.status_code, self.response.text)