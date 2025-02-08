import argparse
import os

from yamlguardian.json_schema_adapter import yaml_to_json_schema
from yamlguardian.save_load_yaml import load_yaml
from yamlguardian.validate import format_errors, validate_openapi_schema
from yamlguardian.yaml_to_json_schema import load_yaml_schemas


def main():
    parser = argparse.ArgumentParser(description="Validate data against a YAML schema.")
    parser.add_argument(
        "-i",
        "--input_file_or_dir",
        type=str,
        help="Path to the YAML data file or directory to validate.",
        required=True,
    )
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

    json_schema = yaml_to_json_schema(schema_dict, "test")
    print("json_schema=", json_schema)
    errors = validate_openapi_schema(json_schema)
    if errors:
        print(f"Validation openapi_schema failed for {args.input_file_or_dir} with the following errors:")
        print(format_errors(errors))
    else:
        print(f"Validation succeeded for {args.input_file_or_dir}.")

    # TODO: validate data against json_schema


if __name__ == "__main__":
    main()
