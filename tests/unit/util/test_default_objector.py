from moco_wrapper.util.objector import DefaultObjector
from moco_wrapper.util.response import ErrorResponse
from moco_wrapper import exceptions as ex

from ..mocks.http import MockHttpErrorResponse



class TestDefaultObjector(object):
    def setup(self):
        self.objector = DefaultObjector()

    def test_unauthorized(self):
        error_resp = MockHttpErrorResponse(401, "test").to_error()

        modified_error = self.objector.convert(error_resp)

        assert isinstance(modified_error, ErrorResponse)
        assert isinstance(modified_error.data, ex.UnauthorizedException)

    def test_forbidden(self):
        error_resp = MockHttpErrorResponse(403, "test").to_error()

        modified_error = self.objector.convert(error_resp)

        assert isinstance(modified_error, ErrorResponse)
        assert isinstance(modified_error.data, ex.ForbiddenException)

    def test_not_fount(self):
        error_resp = MockHttpErrorResponse(404, None).to_error()

        modified_error = self.objector.convert(error_resp)

        assert isinstance(modified_error, ErrorResponse)
        assert isinstance(modified_error.data, ex.NotFoundException)

    def test_unprocessable(self):
        error_resp = MockHttpErrorResponse(422, "test").to_error()

        modified_error = self.objector.convert(error_resp)

        assert isinstance(modified_error, ErrorResponse)
        assert isinstance(modified_error.data, ex.UnprocessableException)

    def test_rate_limit(self):
        error_resp = MockHttpErrorResponse(429, "test").to_error()

        modified_error = self.objector.convert(error_resp)

        assert isinstance(modified_error, ErrorResponse)
        assert isinstance(modified_error.data, ex.RateLimitException)

    def test_server_error(self):
        error_resp = MockHttpErrorResponse(500, None).to_error()

        modified_error = self.objector.convert(error_resp)

        assert isinstance(modified_error, ErrorResponse)
        assert isinstance(modified_error.data, ex.ServerErrorException)
