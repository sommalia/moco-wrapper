import json
from collections import namedtuple

class MWRAPResponse(object):
    """base class for all responses, created by an requestor"""

    def __init__(self, response):
        self.response = response

        self.prefix_key_words = ["from"]

    def _convert_to_object(self, obj):
        for key in obj.keys():
            if key in self.prefix_key_words:
                new_key = '_' + key
                obj[new_key] = obj[key]
                del obj[key]

        return namedtuple('X', obj.keys(), rename=True)(*obj.values())

    def json_to_object(self, content):
        return json.loads(content, object_hook=self._convert_to_object)


    @property 
    def data(self):
        return self.response