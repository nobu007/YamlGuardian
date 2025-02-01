import unittest
import yaml
from yamlguardian.validate import load_yaml_schema, validate_data, format_errors
from yamlguardian.validator import Validator
from yamlguardian.rules import RuleManager

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

    def test_validator_comprehensive_rules(self):
        schema = {
            'root_element': [
                {'name': 'name', 'type': 'string', 'required': True, 'description': 'Name'},
                {'name': 'age', 'type': 'integer', 'required': True, 'description': 'Age'},
                {'name': 'tags', 'type': 'list', 'required': False, 'description': 'Tags'},
                {'name': 'address', 'type': 'object', 'required': False, 'description': 'Address'}
            ]
        }
        validator = Validator(schema)
        data = {'name': 'John', 'age': 30, 'tags': ['tag1', 'tag2'], 'address': {'city': 'Tokyo'}}
        errors = validator.validate(data)
        self.assertEqual(errors, [])

    def test_rule_manager_custom_rules(self):
        def custom_rule(value):
            return value == 'custom_value'

        schema = {
            'root_element': [
                {'name': 'custom_field', 'type': 'string', 'required': True, 'description': 'Custom Field', 'custom_rules': [custom_rule]}
            ]
        }
        rule_manager = RuleManager(schema)
        data = {'custom_field': 'custom_value'}
        errors = rule_manager.validate(data)
        self.assertEqual(errors, [])

        data_invalid = {'custom_field': 'invalid_value'}
        errors_invalid = rule_manager.validate(data_invalid)
        self.assertNotEqual(errors_invalid, [])

if __name__ == '__main__':
    unittest.main()
