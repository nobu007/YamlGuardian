import unittest

import jsonschema
import yaml

from yamlguardian.core import YamlGuardian
from yamlguardian.rules import RuleManager
from yamlguardian.validate import (
    format_errors,
    load_validation_rules,
    validate_data,
    validate_openapi_schema,
    validate_user_defined_yaml,
    validate_user_provided_yaml,
)
from yamlguardian.validator import Validator


class TestValidate(unittest.TestCase):

    def test_load_yaml_schema(self):
        schema = load_validation_rules("tests/rule_config/page_definitions/page1/test_schema.yaml")
        self.assertIsInstance(schema, dict)

    def test_validate_data(self):
        schema = load_validation_rules("tests/rule_config/page_definitions/page1/test_schema.yaml")
        data = {"name": "John", "age": 30}
        errors = validate_data(data, schema)
        self.assertIsNone(errors)

    def test_validate_data_with_errors(self):
        schema = load_validation_rules("tests/rule_config/page_definitions/page1/test_schema.yaml")
        data = {"name": "John"}
        errors = validate_data(data, schema)
        self.assertIsNotNone(errors)

    def test_format_errors(self):
        errors = {"name": ["required field"], "age": ["min value is 18"]}
        formatted_errors = format_errors(errors)
        self.assertIn("name: required field", formatted_errors)
        self.assertIn("age: min value is 18", formatted_errors)

    def test_validator_comprehensive_rules(self):
        schema = {
            "root_element": [
                {"name": "name", "type": "string", "required": True, "description": "Name"},
                {"name": "age", "type": "integer", "required": True, "description": "Age"},
                {"name": "tags", "type": "list", "required": False, "description": "Tags"},
                {"name": "address", "type": "object", "required": False, "description": "Address"},
            ]
        }
        validator = Validator(schema)
        data = {"name": "John", "age": 30, "tags": ["tag1", "tag2"], "address": {"city": "Tokyo"}}
        errors = validator.validate(data)
        self.assertEqual(errors, [])

    def test_rule_manager_custom_rules(self):
        def custom_rule(value):
            return value == "custom_value"

        schema = {
            "root_element": [
                {
                    "name": "custom_field",
                    "type": "string",
                    "required": True,
                    "description": "Custom Field",
                    "custom_rules": [custom_rule],
                }
            ]
        }
        rule_manager = RuleManager(schema)
        data = {"custom_field": "custom_value"}
        errors = rule_manager.validate(data)
        self.assertEqual(errors, [])

        data_invalid = {"custom_field": "invalid_value"}
        errors_invalid = rule_manager.validate(data_invalid)
        self.assertNotEqual(errors_invalid, [])

    def test_yaml_guardian_page_definitions(self):
        yaml_guardian = YamlGuardian(
            schema_file="rule_config/common_definitions/common_definitions.yaml",
            relations_file="rule_config/page_definitions/page1/root_element_relations.yaml",
            common_definitions_file="rule_config/common_definitions/common_definitions.yaml",
        )
        page_data = {
            "root_element": {
                "name": "FormA",
                "type": "form",
                "description": "このフォームはラベルとラジオボタンの関係を定義します。",
                "attributes": {"action": "/submit", "method": "post"},
                "elements": [
                    {
                        "name": "AAA",
                        "type": "label",
                        "description": "このラベルは必須です。",
                        "required": True,
                        "attributes": {"for": "input1"},
                        "check": {"condition": "every", "target": "label"},
                    },
                    {
                        "name": "BBB",
                        "type": "radio",
                        "description": "このラジオボタンはオプションです。",
                        "required": False,
                        "attributes": {"id": "input1", "name": "options"},
                        "prohibited": False,
                        "check": {"condition": "first_only", "target": "radio"},
                    },
                    {
                        "name": "commonLabel",
                        "type": "label",
                        "description": "共通ラベルを使用しています。",
                        "required": True,
                        "attributes": {"for": "commonInput"},
                        "uses_common": True,
                    },
                ],
            }
        }
        errors = yaml_guardian.validate_page(page_data, "rule_config/page_definitions/page1")
        self.assertIsNone(errors)

    def test_validate_data_edge_cases(self):
        schema = load_validation_rules("tests/rule_config/page_definitions/page1/test_schema.yaml")
        data = {"name": "", "age": -1}
        errors = validate_data(data, schema)
        self.assertIsNotNone(errors)
        self.assertIn("name", errors)
        self.assertIn("age", errors)

    def test_format_errors_edge_cases(self):
        errors = {"name": ["required field"], "age": {"min": "min value is 0"}}
        formatted_errors = format_errors(errors)
        self.assertIn("name: required field", formatted_errors)
        self.assertIn("age.min: min value is 0", formatted_errors)

    def test_validate_page_edge_cases(self):
        yaml_guardian = YamlGuardian(
            schema_file="rule_config/common_definitions/common_definitions.yaml",
            relations_file="rule_config/page_definitions/page1/root_element_relations.yaml",
            common_definitions_file="rule_config/common_definitions/common_definitions.yaml",
        )
        page_data = {
            "root_element": {
                "name": "FormA",
                "type": "form",
                "description": "このフォームはラベルとラジオボタンの関係を定義します。",
                "attributes": {"action": "/submit", "method": "post"},
                "elements": [
                    {
                        "name": "AAA",
                        "type": "label",
                        "description": "このラベルは必須です。",
                        "required": True,
                        "attributes": {"for": "input1"},
                        "check": {"condition": "every", "target": "label"},
                    },
                    {
                        "name": "BBB",
                        "type": "radio",
                        "description": "このラジオボタンはオプションです。",
                        "required": False,
                        "attributes": {"id": "input1", "name": "options"},
                        "prohibited": False,
                        "check": {"condition": "first_only", "target": "radio"},
                    },
                    {
                        "name": "commonLabel",
                        "type": "label",
                        "description": "共通ラベルを使用しています。",
                        "required": True,
                        "attributes": {"for": "commonInput"},
                        "uses_common": True,
                    },
                ],
            }
        }
        errors = yaml_guardian.validate_page(page_data, "rule_config/page_definitions/page1")
        self.assertIsNotNone(errors)

    def test_validate_openapi_schema(self):
        input_data = """
        openapi: 3.0.0
        info:
          title: Sample API
          version: 1.0.0
          description: A sample API
        paths:
          /sample:
            get:
              description: Sample GET endpoint
        """
        result = validate_openapi_schema(input_data)
        self.assertEqual(result["message"], "Validation successful")

    def test_validate_user_defined_yaml(self):
        input_data = """
        name: UserDefined
        type: custom
        description: A user defined YAML
        required: true
        attributes:
          key: value
        """
        result = validate_user_defined_yaml(input_data)
        self.assertEqual(result["message"], "Validation successful")

    def test_validate_user_provided_yaml(self):
        input_data = """
        name: UserProvided
        type: custom
        description: A user provided YAML
        required: true
        attributes:
          key: value
        """
        result = validate_user_provided_yaml(input_data)
        self.assertEqual(result["message"], "Validation successful")

    def test_validate_yaml_data(self):
        input_data = """
        name: John
        age: 30
        """
        result = validate_yaml_data(input_data)
        self.assertEqual(result["message"], "Validation successful")

    def test_validate_yaml_data_with_errors(self):
        input_data = """
        name: John
        """
        result = validate_yaml_data(input_data)
        self.assertEqual(result["message"], "Validation failed")
        self.assertIn("errors", result)


if __name__ == "__main__":
    unittest.main()
