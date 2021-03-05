from moco_wrapper.util.response import ListResponse
from ..mocks import http


class TestListResponse(object):
    def setup(self):
        self.items = [1, 2, 3, 4]
        status_code = 200

        self.http_response = http.MockHttpResponse(self.items, status_code)

    def test_iterator(self):
        r = ListResponse(self.http_response)

        for i, item in enumerate(r):
            assert item == self.items[i]

        for i, item in enumerate(r.items):
            assert item == self.items[i]

    def test_getitem(self):
        r = ListResponse(self.http_response)

        assert r[0] == self.items[0]

    def test_len(self):
        r = ListResponse(self.http_response)

        assert len(r) == len(self.items)
