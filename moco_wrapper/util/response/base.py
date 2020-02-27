import json
from collections import namedtuple

class MWRAPResponse(object):
    """base class for all responses, created by an requestor"""

    def __init__(self, response):
        self._response = response


    @property 
    def data(self):
        return self.response

    @property
    def response(self):
        """
        http response object
        """
        return self._response