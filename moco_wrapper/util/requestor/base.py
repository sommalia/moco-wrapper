class BaseRequestor(object):

    @property
    def session(self):
        return None


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
