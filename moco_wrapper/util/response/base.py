import json

class MWRAPResponse(object):
    """base class for all responses, created by an objector"""

    def __init__(self, response):
        self.reponse = response
        self.data = response

    def json_to_object(self, json_content):
        return json.loads(json_content, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))


    @property 
    def data(self):
        return self.data