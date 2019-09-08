import requests
import time

class RateLimitedRequestor(object):

    def __init__(self):
        self.session = requests.Session()

        self.requests_timestamps = []

    def request(self, path, method, params = None, data = None, **kwargs):

        time.sleep(1)

        if method == "GET":
            return self.session.get(path, params=params, data=data, **kwargs)
        elif method == "POST":
            return self.session.post(path, params=params, data=data, **kwargs)
        elif method == "DELETE":
            return self.session.post(path, params=params, data=data, **kwargs)
        elif method == "PUT":
            return self.session.put(path, params=params, data=data, **kwargs)
        elif method == "PATCH":
            return self.session.patch(path, params=params, data=data, **kwargs)

    def get(self, path, params = None, **kwargs):
        return self.request(path, "GET", params=params, **kwargs)

    def post(self, path, data= None, **kwargs):
        return self.request(path, "POST", data=data, **kwargs)

    def put(self, path, data = None, params = None, **kwargs):
        return self.request(path, "PUT", data=data, params=params, **kwargs)

    def delete(self, path, data = None, params = None, **kwargs):
        return self.request(path, "DELETE", data=data, params=params, **kwargs)

    def patch(self, path, data = None, params = None, **kwargs):
        return self.request(path, "PATCH", data=data, params=params, **kwargs)


class TestRequester(RateLimitedRequestor):
    def request(self, path, method, params = None, data = None, **kwargs):
        return {
            "path": path,
            "data" : data,
            "method": method,
            "params" : params,
            "args": kwargs.items()
        }

    