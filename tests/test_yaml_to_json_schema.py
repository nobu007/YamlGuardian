import unittest
from yamlguardian.yaml_to_json_schema import yaml_to_json_schema, load_yaml_file

class TestConvertYamlToJsonSchema(unittest.TestCase):

    def test_convert_name_field(self):
        yaml_schema = {
            'name': {'type': 'string', 'minlength': 1, 'maxlength': 50, 'required': True}
        }
        json_schema = yaml_to_json_schema(yaml_schema)
        self.assertEqual(json_schema['properties']['name']['type'], 'string')
        self.assertEqual(json_schema['properties']['name']['minLength'], 1)
        self.assertEqual(json_schema['properties']['name']['maxLength'], 50)
        self.assertIn('name', json_schema['required'])

    def test_convert_age_field(self):
        yaml_schema = {
            'age': {'type': 'integer', 'min': 0, 'required': True}
        }
        json_schema = yaml_to_json_schema(yaml_schema)
        self.assertEqual(json_schema['properties']['age']['type'], 'integer')
        self.assertIn('age', json_schema['required'])

class TestLoadYamlFile(unittest.TestCase):

    def test_load_yaml_file(self):
        yaml_content = load_yaml_file('tests/rule_config/page_definitions/page1/test_schema.yaml')
        self.assertIsInstance(yaml_content, dict)

if __name__ == '__main__':
    unittest.main()
