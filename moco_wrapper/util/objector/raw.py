from .base import BaseObjector

class RawObjector(BaseObjector):
    """Objector class that does no conversion (for testing purposes)"""
    
    def convert(self, response):
        """Returns the response object that was given

        :param response: response object to convert
        :returns: response object that was the parameter
        """
        return response