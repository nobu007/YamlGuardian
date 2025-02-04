import yaml
import jsonschema
import os
from pathlib import Path
from ruamel.yaml import YAML
from yamlguardian.validator import Validator

yaml = YAML()


def load_yaml(yaml_file_or_contents: str) -> dict:
    """
    Load YAML file and return a dictionary containing the file's content.

    Args:
        yaml_file_or_contents (str): path or contents of the YAML

    Returns:
        dict | None: a dictionary containing the YAML's content, or throws an exception.
    """
    if isinstance(yaml_file_or_contents, (str, Path)) and Path(yaml_file_or_contents).is_file():
        with open(yaml_file_or_contents, "r", encoding="utf-8") as f:
            schema = yaml.load(f)
    else:
        schema = yaml.load(yaml_file_or_contents)
    return schema


def save_yaml(data: dict, yaml_file: str):
    """
    Save a dictionary to a YAML file.

    Args:
        data (dict): the data to save
        yaml_file (str): the path to the YAML file
    """
    prepare_dir(yaml_file)
    with open(yaml_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f)


def prepare_dir(output_file_path):
    directory = os.path.dirname(output_file_path)
    os.makedirs(directory, exist_ok=True)


def validate_data(data, schema):
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        return str(e)
    return None


def format_errors(errors):
    formatted_errors = []
    for field, error in errors.items():
        if isinstance(error, list):
            for e in error:
                formatted_errors.append(f"{field}: {e}")
        elif isinstance(error, dict):
            for subfield, suberror in error.items():
                formatted_errors.append(f"{field}.{subfield}: {suberror}")
    return "\n".join(formatted_errors)


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
        schema = load_yaml("schema.yaml")
        errors = validate_data(data, schema)
        if errors:
            return {"message": "Validation failed", "errors": format_errors(errors)}
        return {"message": "Validation successful"}
    except Exception as e:
        return {"message": "Validation error", "detail": str(e)}


def validate_openapi_schema(input_data):
    try:
        validation_rules = yaml.safe_load(input_data)
        schema = load_yaml("openapi_schema.yaml")
        v = Validator(schema)
        if not v.validate(validation_rules):
            return {"message": "Validation failed", "errors": v.errors}
        return {"message": "Validation successful"}
    except Exception as e:
        return {"message": "Validation error", "detail": str(e)}


def validate_user_defined_yaml(input_data):
    try:
        data = yaml.safe_load(input_data)
        schema = load_yaml("user_defined_yaml.yaml")
        v = Validator(schema)
        if not v.validate(data):
            return {"message": "Validation failed", "errors": v.errors}
        return {"message": "Validation successful"}
    except Exception as e:
        return {"message": "Validation error", "detail": str(e)}


def validate_user_provided_yaml(input_data):
    try:
        data = yaml.safe_load(input_data)
        schema = load_yaml("user_provided_yaml.yaml")
        v = Validator(schema)
        if not v.validate(data):
            return {"message": "Validation failed", "errors": v.errors}
        return {"message": "Validation successful"}
    except Exception as e:
        return {"message": "Validation error", "detail": str(e)}
