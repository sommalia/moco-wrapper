from .base import BaseRequestor

class RawRequestor(BaseRequestor):
    def request(self, path, method, params = None, data = None, **kwargs):
        return {
            "path": path,
            "data" : data,
            "method": method,
            "params" : params,
            "args": kwargs.items()
        }
