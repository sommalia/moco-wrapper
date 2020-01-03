from .base import MWRAPResponse
import json

class ListingResponse(MWRAPResponse):
    """
    Class for handling responses where the body can be converted into valid json AND are listings (collections of objects)
    """

    @property 
    def items(self):
        """
        Returns the list of objects the response contains
        """
        return self._items

    
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
        """
        return self._items
    

    def __init__(self, response):
        """
        class constructor

        :param response: response object
        """
        super(ListingResponse, self).__init__(response)

        #loop over every single item in the json dictionary and convert it into an object by itself
        json_content = response.json()
        self._items = []
        for json_item in json_content:
            self._items.append(self.json_to_object(json.dumps(json_item)))

        