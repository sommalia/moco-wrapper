class Endpoint(object):
    def __init__(
        self,
        slug: str,
        url_template: str,
        http_method: str,
        objector_model_type=None
    ):
        """
        Class constructor for Endpoint object

        :param slug: Unique slug for this endpoint
        :param url_template: Url Path this Endpoint uses
        :param http_method: Http method this endpoint uses
        :param objector_model_type: Type of objector model this endpoint returns

        :type slug: str
        :type url_template: str
        :type http_method: str
        :type objector_model_type: type
        """

        self.slug = slug
        self.url_template = url_template
        self.objector_model_type = objector_model_type
        self.method = http_method

    def url_format(self, params=None):
        """
        Retrieves the url to use for accessing the api

        :param params: Dictionary of url parameters

        :type params: dict (default ``None``)

        :returns: Url path
        :rtype: str


        .. note::

            If the Endpoint uses an url template like /projects/{id}/assigned, url format will return
            the final url to use

        .. code-block:: python

            >> e = Endpoint("my_endpoint", "/projects/{id}/assigned", "GET")
            >> params = { "id": 44 }
            >> e.url_format(params)
            '/projects/44/assigned'

        """
        if params is None:
            return self.url_template
        else:
            return self.url_template.format(**params)

    @property
    def type(self):
        return self.objector_model_type
