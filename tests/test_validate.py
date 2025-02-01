import unittest
import yaml
from yamlguardian.validate import load_yaml_schema, validate_data, format_errors

class TestValidate(unittest.TestCase):

    def test_load_yaml_schema(self):
        schema = load_yaml_schema('tests/test_schema.yaml')
        self.assertIsInstance(schema, dict)

    def test_validate_data(self):
        schema = load_yaml_schema('tests/test_schema.yaml')
        data = {'name': 'John', 'age': 30}
        errors = validate_data(data, schema)
        self.assertIsNone(errors)

    def test_validate_data_with_errors(self):
        schema = load_yaml_schema('tests/test_schema.yaml')
        data = {'name': 'John'}
        errors = validate_data(data, schema)
        self.assertIsNotNone(errors)

    def test_format_errors(self):
        errors = {'name': ['required field'], 'age': ['min value is 18']}
        formatted_errors = format_errors(errors)
        self.assertIn('name: required field', formatted_errors)
        self.assertIn('age: min value is 18', formatted_errors)

if __name__ == '__main__':
    unittest.main()
