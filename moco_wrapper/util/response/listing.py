from .base import MWRAPResponse
import json

class ListingResponse(MWRAPResponse):

    @property 
    def items(self):
        return self._items

    @property 
    def next(self):
        pass

    @property
    def before(self):
        pass

    @property
    def data(self):
        return self._items
    

    def __init__(self, response):
        super(ListingResponse, self).__init__(response)

        #get object contents
        json_content = response.json()
        self._items = []
        for json_item in json_content:
            print(json_item)
            self._items.append(self.json_to_object(json.dumps(json_item)))

        