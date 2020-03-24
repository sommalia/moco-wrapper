from moco_wrapper.util.requestor.base import BaseRequestor

class TestDefaultRequestor(object):

    def setup(self):
        self.requestor = BaseRequestor()

    def test_query_string_bool_conversion(self):
        params = {
            "str_param" : "this is a string",
            "int_param": 1,
            "bool_param": True
        }

        new_params = self.requestor._format_params(params)

        assert new_params["str_param"] == params["str_param"]
        assert new_params["int_param"] == params["int_param"]

        assert new_params["bool_param"] != params["bool_param"]
        assert new_params["bool_param"] == "true"
