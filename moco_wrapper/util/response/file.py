from .base import MWRAPResponse

class FileResponse(MWRAPResponse):
    """
    Class for handling responses where the body is just binary content representing a file
    """

    @property 
    def data(self):
        """
        Returns the binary data of the response
        """
        return self._data

    @property
    def file(self):
        """
        Returns the binary data of the response
        """
        return self.data

    def write_to_file(self, file_path):
        """
        Writes the response content to a file

        :param file_path: path of the target file
        """

        with open(file_path, 'w+b') as bf:
            binary_format = bytearray(self.data)
            bf.write(binary_format)

    

    def __init__(self, response):
        """
        class constructor

        :param response: response object
        """
        super(FileResponse, self).__init__(response)

        self._data = response.content

    def __str__(self):
        return "<FileResponse, Status Code: {}, Data: binary_content>".format(self.response.status_code)