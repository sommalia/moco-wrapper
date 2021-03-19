from moco_wrapper import models as m
from moco_wrapper.util.endpoint import Endpoint


class EndpointManager(object):
    """
    Class for managing all endpoints that the moco class uses
    """
    def __init__(self):
        """
        Class constructor
        """
        self.map = {}

        self.endpoints = []
        self.endpoints.extend(m.Session.endpoints())

        self.build_map()

    def build_map(self):
        """
        Build as dictionary from the list of endpoints
        """
        for endpoint in self.endpoints:
            self.map[endpoint.slug] = endpoint

    def get(self, slug) -> Endpoint:
        """
        Retrieve an endpoint by its unique slug

        :param slug: Endpoint slug

        :type slug: str

        :return: Endpoint with the given slug, or None if the endpoint does not exist
        """
        return self.map.get(slug, None)
