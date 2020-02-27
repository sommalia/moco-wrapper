from .base import MWRAPResponse
from json import dumps

class ListingResponse(MWRAPResponse):
    """
    Class for handling http responses where the response body is a json list
    """

    @property 
    def items(self):
        """
        Get the list of objects the response contains

        .. code-block:: python

            m = Moco()
            project_list = m.Project.getlist()

            for item in project_list.items:
                print(item)

        .. seealso:: 

            :attr:`data`

        """
        return self._data

    
    @property
    def x_page(self):
        pass

    @property 
    def x_per_page(self):
        pass

    @property
    def x_total(self):
        pass

    @property
    def is_last(self):
        pass


    @property
    def data(self):
        """
        Returns the list of object the response contains

        .. seealso:: 

            :attr:`items`
        """
        return self._data
    

    def __init__(self, response):
        """
        class constructor

        :param response: http response object
        """
        super(ListingResponse, self).__init__(response)

        #loop over every single item in the json dictionary and convert it into an object by itself
        json_content = response.json()
        items = []
        for json_item in json_content:
            items.append(json_item)

        self._data = items

    def __str__(self):
         return "<ListingResponse, Status Code: {}, Data: {}>".format(self.response.status_code, str(self._data))

        