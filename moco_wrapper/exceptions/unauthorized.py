from .base import MocoException

class UnauthorizedException(MocoException):

    def __str__(self):
        return "<UnauthorizedException, Status Code: {}, Data: {}>".format(self.http_response.status_code, self.data)
