class UnauthorizedException(BaseException):
    def __init__(self, http_response, data):
        self.http_response = http_response
        self.data = data

    def __str__(self):
        return "<UnauthorizedException, Status Code: {}, Msg: {}>".format(self.http_response.status_code, self.data)
