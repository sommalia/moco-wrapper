from moco_wrapper.util.response.base import MWRAPResponse
from moco_wrapper import exceptions

class ErrorResponse(MWRAPResponse):
    """
    class for handling error messages returned by the api
    """

    @property
    def is_recoverable(self) -> bool:
        """
        Checks the http status code of the response and returns True if the error is not a permanent error, i.e. recovering is possible by simply waiting a bit and sending the request again.

        :type: bool
        :returns: ``True`` if recovery is possible by sending the request again later, otherwise ``False``

        .. code-block:: python

            m = Moco()
            project_id = 22

            project_get = m.Project.get(project_id)

            if isinstance(project_get, ErrorResponse) and project_get.is_recoverable:
                time.sleep(5)
                project_get = m.Project.get(project_id)
            
            print(project_get)
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

        return self._data

    def __str__(self):
        return "<ErrorResponse, Status Code: {}, Data: {}>".format(self.response.status_code, self.data)
    
    def __init__(self, response):
        """
        class constructor

        :param response: response object
        """
        super(ErrorResponse, self).__init__(response)

        #set data to the error message
        self._data = self.response.text