import json
from collections import namedtuple

class MWRAPResponse(object):
    """base class for all responses, created by an requestor"""

    def __init__(self, response):
        self.response = response

    @property 
    def data(self):
        return self.response