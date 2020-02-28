class BaseRequestor(object):
    """
    Base class all other Requestor classes inherit from
    """
    
    ERROR_STATUS_CODES = [400, 401, 403, 404, 422, 429]
    SUCCESS_STATUS_CODES =  [200, 201, 204]

    @property
    def session(self):
        return None


    def get(self, path, params = None, **kwargs):
        return self.request("GET", path, params=params, **kwargs)

    def post(self, path, data= None, **kwargs):
        return self.request("POST", path, data=data, **kwargs)

    def put(self, path, data = None, params = None, **kwargs):
        return self.request("PUT", path, data=data, params=params, **kwargs)

    def delete(self, path, data = None, params = None, **kwargs):
        return self.request("DELETE", path, data=data, params=params, **kwargs)

    def patch(self, path, data = None, params = None, **kwargs):
        return self.request("PATCH", path, data=data, params=params, **kwargs)
