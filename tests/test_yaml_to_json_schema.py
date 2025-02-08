import unittest

from yamlguardian.yaml_to_json_schema import load_yaml_schemas, yaml_to_json_schema


class TestConvertYamlToJsonSchema(unittest.TestCase):
    def test_convert_name_field(self):
        yaml_schema = {"name": {"type": "string", "minlength": 1, "maxlength": 50, "required": True}}
        json_schema = yaml_to_json_schema(yaml_schema)
        assert json_schema["properties"]["name"]["type"] == "string"
        assert json_schema["properties"]["name"]["minLength"] == 1
        assert json_schema["properties"]["name"]["maxLength"] == 50
        assert "name" in json_schema["required"]

    def test_convert_age_field(self):
        yaml_schema = {"age": {"type": "integer", "min": 0, "required": True}}
        json_schema = yaml_to_json_schema(yaml_schema)
        assert json_schema["properties"]["age"]["type"] == "integer"
        assert "age" in json_schema["required"]


class TestLoadYamlFile(unittest.TestCase):
    def test_load_yaml_file(self):
        yaml_content = load_yaml_schemas("tests/rule_config/page_definitions/page1")
        assert isinstance(yaml_content, dict)


if __name__ == "__main__":
    unittest.main()
