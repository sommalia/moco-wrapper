
class MWRAPResponse(object):
    """
    Base class for all responses created by a requestor
    """

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
