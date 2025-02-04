import argparse
import yaml
import os
from yamlguardian.validate import load_validation_rules
from yamlguardian.validate import validate_data
from yamlguardian.validate import format_errors
from yamlguardian.json_schema_adapter import yaml_to_json_schema
from yamlguardian.yaml_to_json_schema import load_yaml_schemas
from yamlguardian.save_load_yaml import load_yaml


def main():
    parser = argparse.ArgumentParser(description="Validate data against a YAML schema.")
    parser.add_argument("-i", "--input_file_or_dir", type=str, help="Path to the YAML data file or directory to validate.", required=True)
    parser.add_argument(
        "-s",
        "--schema_file_or_dir",
        type=str,
        help="Path to the YAML schema file or directory.",
        default="rule_config",
        required=False,
    )

    args = parser.parse_args()

    # schema_dict
    if os.path.isdir(args.input_file_or_dir):
        input_dir = args.input_file_or_dir
        schema_dict = load_yaml_schemas(input_dir)
    else:
        input_file = args.input_file_or_dir
        schema_name = os.path.splitext(os.path.basename(input_file))[0]
        schema_dict = {}
        schema_dict[schema_name] = load_yaml(input_file)

    yaml_schema = load_validation_rules(args.schema_file_or_dir)
    cerberus_schema = convert_yaml_to_cerberus(yaml_schema)
    errors = validate_data(data, cerberus_schema)
    if errors:
        print(f"Validation failed for {file} with the following errors:")
        print(format_errors(errors))
    else:
        print(f"Validation succeeded for {file}.")



if __name__ == "__main__":
    main()
