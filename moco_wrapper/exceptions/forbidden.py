from .base import MocoException

class ForbiddenException(MocoException):
    def __str__(self):
        return "<ForbiddenException, Status Code: {}, Data: {}>".format(self.http_response.status_code, self.data)
        