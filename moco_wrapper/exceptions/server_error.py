from .base import MocoException

class ServerErrorException(MocoException):
        
    def __str__(self):
        return "<ServerErrorException, Status Code: {}>".format(self.http_response.status_code)
        