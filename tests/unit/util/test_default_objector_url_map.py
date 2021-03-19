from moco_wrapper.util.objector import DefaultObjector


class TestDefaultObjectorUrlMappings(object):

    def _build_request_url(self, path):
        return "https://example.org/api/v1/" + path

    def test_base_class(self):
        url = self._build_request_url("projects")

        expected_class = "ProjectBaseClass"
        objector = DefaultObjector()
        objector.class_map = {
            "projects": {
                "base": expected_class,
                "other": "OtherClassName"
            }
        }

        class_name = objector.get_class_name_from_request_url(url=url)

        assert class_name == expected_class

    def test_specific_class(self):
        url = self._build_request_url("projects/other")
        expected_class = "ProjectOtherClass"

        objector = DefaultObjector()
        objector.class_map = {
            "projects": {
                "base": "ProjectBaseClass",
                "other": expected_class
            }
        }

        class_name = objector.get_class_name_from_request_url(url)

        assert class_name == expected_class
