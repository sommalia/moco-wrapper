from .base import MWRAPResponse


class EmptyResponse(MWRAPResponse):
    """
    Class for handling responses where the body contains no content but the operation on the api was a success (likely a delete operation)
    """

    def __init__(self, response):
        """
        Class constructor

        :param response: http response object
        """
        super(EmptyResponse, self).__init__(response)

    @property
    def data(self):
        """
        No data in an empty response, returns None

        :returns: ``None``
        """
        return None

    def __str__(self):
        return "<EmptyResponse, Status Code: {}>".format(self.response.status_code)
