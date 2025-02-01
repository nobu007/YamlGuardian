import yaml
from cerberus import Validator

def load_yaml_schema(file_path):
    with open(file_path, 'r') as file:
        schema = yaml.safe_load(file)
    return schema

def validate_data(data, schema):
    v = Validator(schema)
    if not v.validate(data):
        return v.errors
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
