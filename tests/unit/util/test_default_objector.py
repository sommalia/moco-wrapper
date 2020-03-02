from moco_wrapper.util.objector import DefaultObjector
from moco_wrapper.util.response import ErrorResponse
from moco_wrapper import exceptions as ex

class FakeErrorResponse(object):
    def __init__(self, response_status_code, response_data):
        self.status_code = response_status_code
        self.text = response_data

    def to_error(self):
        return ErrorResponse(self)


class TestDefaultObjector(object):
    def setup(self):
        self.objector = DefaultObjector()


    def test_unauthorized(self):
        error_resp = FakeErrorResponse(401, "test").to_error()

        modified_error = self.objector.convert(error_resp)

        assert isinstance(modified_error, ErrorResponse)
        assert isinstance(modified_error.data, ex.UnauthorizedException)

    def test_forbidden(self):
        error_resp = FakeErrorResponse(403, "test").to_error()

        modified_error = self.objector.convert(error_resp)

        assert isinstance(modified_error, ErrorResponse)
        assert isinstance(modified_error.data, ex.ForbiddenException)

    def test_not_fount(self):
        error_resp = FakeErrorResponse(404, None).to_error()

        modified_error = self.objector.convert(error_resp)

        assert isinstance(modified_error, ErrorResponse)
        assert isinstance(modified_error.data, ex.NotFoundException)

    
    def test_unprocessable(self):
        error_resp = FakeErrorResponse(422, "test").to_error()

        modified_error = self.objector.convert(error_resp)

        assert isinstance(modified_error, ErrorResponse)
        assert isinstance(modified_error.data, ex.UnprocessableException)

    def test_rate_limit(self):
        error_resp = FakeErrorResponse(429, "test").to_error()

        modified_error = self.objector.convert(error_resp)

        assert isinstance(modified_error, ErrorResponse)
        assert isinstance(modified_error.data, ex.RateLimitException)

    
    def test_server_error(self):
        error_resp = FakeErrorResponse(500, None).to_error()

        modified_error = self.objector.convert(error_resp)

        assert isinstance(modified_error, ErrorResponse)
        assert isinstance(modified_error.data, ex.ServerErrorException)
