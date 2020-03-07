from .base import MWRAPResponse

class FileResponse(MWRAPResponse):
    """
    Class for handling http responses where the body is just binary content representing a file
    """

    @property 
    def data(self):
        """
        Returns the binary data of the response

        
        .. seealso::

            :attr:`file`

        """
        return self._data

    @property
    def file(self):
        """
        Returns the binary data of the response

        .. code-block:: python

            m = Moco()
            offer_id = 22
            target_path = "./offer.pdf"

            file_response = m.Offer.pdf(offer_id)
            with open(target_path, "w+b") as f:
                f.write(file_response.file)

        .. seealso::

            :attr:`data`

        """
        return self._data

    def write_to_file(
        self,
        file_path: str
        ):
        """
        Writes the binary response content to a file

        :param file_path: path of the target file

        .. code-block:: python

            m = Moco()
            offer_id = 22
            target_path = "./offer.pdf"

            file_response = m.Offer.pdf(offer_id)
            file_response.write_to_file(target_path)

        """

        with open(file_path, 'w+b') as bf:
            bf.write(self._data)

    def __init__(
        self, 
        response
        ):
        """
        class constructor

        :param response: http response object
        """
        super(FileResponse, self).__init__(response)

        binary_format = bytearray(response.content)
        self._data = binary_format

    def __str__(self):
        return "<FileResponse, Status Code: {}, Data: binary_content>".format(self.response.status_code)