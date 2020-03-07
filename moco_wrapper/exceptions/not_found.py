from .base import MocoException

class NotFoundException(MocoException):
    
    def __str__(self):
        return "<NotFoundException, Status Code: {}>".format(self.http_response.status_code)
        