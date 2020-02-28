from moco_wrapper import exceptions
from moco_wrapper.util.response import ErrorResponse

class FakeResponse(object):
    def __init__(self, status_code, text = None):
        self.status_code = status_code
        self.text = text

class TestErrorResponse(object):
    def test_unauthorized(self):
        response = ErrorResponse(FakeResponse(401))
        ex = response.to_exception()

        assert isinstance(ex, exceptions.UnauthorizedException)

    def test_forbidden(self):
        response = ErrorResponse(FakeResponse(403))
        ex = response.to_exception()

        assert isinstance(ex, exceptions.ForbiddenException)

    def test_not_found(self):
        response = ErrorResponse(FakeResponse(404))
        ex = response.to_exception()

        assert isinstance(ex, exceptions.NotFoundException)

    def test_unprocessable(self):
        response = ErrorResponse(FakeResponse(422))
        ex = response.to_exception()

        assert isinstance(ex, exceptions.UnprocessableException)

    def test_rate_limit(self):
        response = ErrorResponse(FakeResponse(429))
        ex = response.to_exception()

        assert isinstance(ex, exceptions.RateLimitException)

    
    def test_server_error(self):
        response = ErrorResponse(FakeResponse(500))
        ex = response.to_exception()

        assert isinstance(ex, exceptions.ServerErrorException)