from moco_wrapper.util.response import ErrorResponse


class MockHttpResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class MockHttpErrorResponse(object):
    def __init__(self, response_status_code, response_data):
        self.status_code = response_status_code
        self.text = response_data

    def to_error(self):
        return ErrorResponse(self)
