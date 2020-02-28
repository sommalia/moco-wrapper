class UnprocessableException(BaseException):
    def __init__(self, http_response, data):
        self.http_response = http_response
        self.data = data

    @property
    def response(self):
        return self.http_response

    def __str__(self):
        return "<UnprocessableException, Status Code: {}, Data: {}>".format(self.http_response.status_code, self.data)