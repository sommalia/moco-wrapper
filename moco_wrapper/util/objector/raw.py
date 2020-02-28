from .base import BaseObjector

class RawObjector(BaseObjector):
    """
    Objector class that does no conversion (for testing purposes)
    """
    
    def convert(self, requestor_response):
        """
        Returns the response object that was given to it.

        :param requestor_response: Response object to convert
        :returns: ``requestor_response`` as it is
        """
        return requestor_response