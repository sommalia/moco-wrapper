from moco_wrapper.util.endpoint import Endpoint

class MockObjectorModel(object):
    def __init__(self):
        self.test_value = 1

class TestEndpoint(object):

    def test_url_template(self):
        id = 44
        value = 55

        template = "/ba/{id}/ha/{value}"
        url_expected = template.format(id=id, value=value)

        e = Endpoint("test_slug", template, "GET")
        e_params = {
            "id": id,
            "value": value
        }

        assert e.url_format(e_params) == url_expected

    def test_objector_model(self):
        e = Endpoint("test-slug", "test/template/", "GET", MockObjectorModel)

        assert e.type == MockObjectorModel

    def test_objector_model_empty(self):
        e = Endpoint("test-slug", "test/template", "GET")

        assert e.type is None
