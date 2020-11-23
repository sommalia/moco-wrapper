from .base import MWRAPResponse


class ObjectResponse(MWRAPResponse):
    """
    Class for handling http responses where the body is a single object
    """

    @property
    def data(self) -> object:
        """
        Returns the json data of the response as a dictionary

        .. code-block:: python

            m = Moco()
            project_id = 22

            json_response = m.Project.get(project_id).data
            print(json_response)

        """
        return self._data

    def __init__(self, response):
        """
        class constructor

        :param response: http response object
        """
        super(ObjectResponse, self).__init__(response)

        self._data = self.response.json()

    def __str__(self):
        return "<ObjectResponse, Status Code: {}, Data: {}>".format(self.response.status_code, str(self._data))
