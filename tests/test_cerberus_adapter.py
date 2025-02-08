import unittest

from yamlguardian.cerberus_adapter import convert_yaml_to_cerberus
from yamlguardian.save_load_yaml import load_yaml


class TestConvertYamlToCerberus(unittest.TestCase):
    def test_convert_name_field(self):
        yaml_schema = {"name": {"type": "string", "minlength": 1, "maxlength": 50, "required": True}}
        cerberus_schema = convert_yaml_to_cerberus(yaml_schema)
        assert cerberus_schema["name"]["type"] == "string"
        assert cerberus_schema["name"]["minlength"] == 1
        assert cerberus_schema["name"]["maxlength"] == 50
        assert cerberus_schema["name"]["required"] == True

    def test_convert_age_field(self):
        yaml_schema = {"age": {"type": "integer", "min": 0, "required": True}}
        cerberus_schema = convert_yaml_to_cerberus(yaml_schema)
        assert cerberus_schema["age"]["type"] == "integer"
        assert cerberus_schema["age"]["min"] == 0
        assert cerberus_schema["age"]["required"] == True


class TestLoadYamlFile(unittest.TestCase):
    def test_load_yaml_file(self):
        yaml_content = load_yaml("tests/rule_config/page_definitions/page1/test_schema.yaml")
        assert isinstance(yaml_content, dict)


if __name__ == "__main__":
    unittest.main()
