class ServerErrorException(BaseException):
    def __init__(self, http_response):
        self.http_response = http_response

    def __str__(self):
        return "<ServerErrorException, Status Code: {}>".format(self.http_response.status_code)