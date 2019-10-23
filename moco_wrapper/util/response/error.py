from .base import MWRAPResponse


class ErrorResponse(MWRAPResponse):
    """
    class for handling responses by the api that are containing errors
    """

    @property
    def is_recoverable(self):
        """
        Checks the http status code of the response and returns True if the error is not a permanent error, i.e. recovering is possible by simply waiting a bit and sending the request again.

        :returns: True if recovery is possible by sending the request again later, False if not
        """

        if self.response.status_code == 429: 
            #429 is the status code for too many requests, any other error status code means the request (or the user) is at fault
            return True
        else:
            return False

    @property
    def data(self):
        """
        Returns the text of the object (the error message itself)
        """

        return self.response.text
    
    def __init__(self, response):
        """
        class constructor

        :param response: response object
        """
        super(ErrorResponse, self).__init__(response)