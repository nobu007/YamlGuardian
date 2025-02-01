import yaml
import jsonschema
from cerberus import Validator

def load_yaml_schema(file_path):
    with open(file_path, 'r') as file:
        schema = yaml.safe_load(file)
    return schema

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
        schema = load_yaml_schema('schema.yaml')
        errors = validate_data(data, schema)
        if errors:
            return {"message": "Validation failed", "errors": format_errors(errors)}
        return {"message": "Validation successful"}
    except Exception as e:
        return {"message": "Validation error", "detail": str(e)}

def validate_openapi_schema(input_data):
    try:
        data = yaml.safe_load(input_data)
        schema = load_yaml_schema('openapi_schema.yaml')
        v = Validator(schema)
        if not v.validate(data):
            return {"message": "Validation failed", "errors": v.errors}
        return {"message": "Validation successful"}
    except Exception as e:
        return {"message": "Validation error", "detail": str(e)}
