class Endpoint(object):
    def __init__(
        self,
        slug: str,
        url_template: str,
        method: str,
        objector_model_type=None
    ):
        self.slug = slug
        self.url_template = url_template
        self.method = method
        self.objector_model_type = objector_model_type

    def url_format(self, **kwargs):
        return self.url_template.format(**kwargs)

    @property
    def type(self):
        return self.objector_model_type
