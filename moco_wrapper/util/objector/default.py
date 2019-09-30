from .base import BaseObjector

class DefaultObjector(BaseObjector):
    def __init__(self):
        pass

    def convert(self, response):
        """converts a request.response object into an mwrap object"""
        return response