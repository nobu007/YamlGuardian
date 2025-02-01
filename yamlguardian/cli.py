import argparse
import yaml
from yamlguardian.validate import load_yaml_schema
from yamlguardian.validate import validate_data
from yamlguardian.validate import format_errors
from yamlguardian.cerberus_adapter import convert_yaml_to_cerberus, load_yaml_file

def main():
    parser = argparse.ArgumentParser(description='Validate data against a YAML schema.')
    parser.add_argument('data', type=str, help='Path to the YAML data file.')
    parser.add_argument('schema', type=str, help='Path to the YAML schema file.')
    args = parser.parse_args()

    data = load_yaml_file(args.data)
    yaml_schema = load_yaml_schema(args.schema)
    cerberus_schema = convert_yaml_to_cerberus(yaml_schema)
    errors = validate_data(data, cerberus_schema)

    if errors:
        print("Validation failed with the following errors:")
        print(format_errors(errors))
    else:
        print("Validation succeeded.")

if __name__ == "__main__":
    main()
