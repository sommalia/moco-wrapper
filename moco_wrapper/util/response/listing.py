from .base import MWRAPResponse

class ListingReponse(MWRAPResponse):

    @property 
    def items(self):
        return self.items

    @property 
    def next(self):
        pass

    @property
    def before(self):
        pass

    @property
    def data(self):
        return self.items
    

    def __init__(self, response):
        super(MWRAPResponse,response).__init()

        #get object contents
        json_content = response.json()
        self.items = []
        for json_item in content:
            self.items.append(self.json_to_object(json_item))

        