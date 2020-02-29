class MocoException(BaseException):
    """
    Base Exceptions all other exceptions used in this package inherit from
    """
    def __init__(self, http_response, data):
        self.http_response = http_response
        self.data = data

    @property
    def response(self):
        return self.http_response