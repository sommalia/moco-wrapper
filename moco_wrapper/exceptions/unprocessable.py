from .base import MocoException

class UnprocessableException(MocoException):

    def __str__(self):
        return "<UnprocessableException, Status Code: {}, Data: {}>".format(self.http_response.status_code, self.data)
        