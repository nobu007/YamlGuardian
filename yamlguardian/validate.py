import os

import jsonschema
import yaml
from cerberus import Validator

from yamlguardian.directory_analyzer import DirectoryAnalyzer
from yamlguardian.save_load_yaml import format_errors
from yamlguardian.yaml_json_converter import YamlJsonConverter


def load_validation_rules(file_or_dir_path: str) -> dict | None:
    validation_schema = None
    if os.path.isfile(file_or_dir_path):
        with open(file_or_dir_path, encoding="utf-8") as file:
            validation_schema = yaml.safe_load(file)
    else:
        # Load all yaml files in the directory
        analyzer = DirectoryAnalyzer()
        validation_schema = analyzer.analyze_directory_structure(file_or_dir_path)
    return validation_schema


def validate_data(data, schema) -> str:
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        print("validate_data ValidationError: e=", e)
        return [str(e)]
    return []  # no error


def validate_yaml_data(input_data):
    try:
        data = yaml.safe_load(input_data)
        openapi_validation_result = validate_openapi_schema(input_data)
        if openapi_validation_result["message"] == "Validation failed":
            return openapi_validation_result
        user_defined_validation_result = validate_user_defined_yaml(input_data)
        if user_defined_validation_result["message"] == "Validation failed":
            return user_defined_validation_result
        user_provided_validation_result = validate_user_provided_yaml(input_data)
        if user_provided_validation_result["message"] == "Validation failed":
            return user_provided_validation_result
        schema = load_validation_rules("schema.yaml")
        json_schema = YamlJsonConverter.yaml_to_json(schema)
        errors = validate_data(data, json_schema)
        if errors:
            return {"message": "Validation failed", "errors": format_errors(errors)}
        return {"message": "Validation successful"}
    except Exception as e:
        return {"message": "Validation error", "detail": str(e)}


def validate_openapi_schema(input_data):
    try:
        validation_rules = yaml.safe_load(input_data)
        schema = load_validation_rules("openapi_schema.yaml")
        v = Validator(schema)
        if not v.validate(validation_rules):
            return {"message": "Validation failed", "errors": v.errors}
        return {"message": "Validation successful"}
    except Exception as e:
        return {"message": "Validation error", "detail": str(e)}


def validate_user_defined_yaml(input_data):
    try:
        data = yaml.safe_load(input_data)
        schema = load_validation_rules("user_defined_yaml.yaml")
        v = Validator(schema)
        if not v.validate(data):
            return {"message": "Validation failed", "errors": v.errors}
        return {"message": "Validation successful"}
    except Exception as e:
        return {"message": "Validation error", "detail": str(e)}


def validate_user_provided_yaml(input_data):
    try:
        data = yaml.safe_load(input_data)
        schema = load_validation_rules("user_provided_yaml.yaml")
        v = Validator(schema)
        if not v.validate(data):
            return {"message": "Validation failed", "errors": v.errors}
        return {"message": "Validation successful"}
    except Exception as e:
        return {"message": "Validation error", "detail": str(e)}
