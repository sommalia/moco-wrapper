import json
from collections import namedtuple

class MWRAPResponse(object):
    """base class for all responses, created by an requestor"""

    def __init__(self, response):
        self.response = response

    def json_to_object(self, content):
        return json.loads(content, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))


    @property 
    def data(self):
        return self.response