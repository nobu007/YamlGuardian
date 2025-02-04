import argparse
import yaml
from yamlguardian.validate import load_validation_rules
from yamlguardian.validate import validate_data
from yamlguardian.validate import format_errors
from yamlguardian.cerberus_adapter import convert_yaml_to_cerberus
from yamlguardian.load_yaml import load_yaml_file


def main():
    parser = argparse.ArgumentParser(description="Validate data against a YAML schema.")
    parser.add_argument("-i", "--data", type=str, help="Path to the YAML data file to validate.")
    parser.add_argument(
        "-s",
        "--schema",
        type=str,
        help="Path to the YAML schema dir.",
        default="/home/jinno/drill/gamebook/codeinterpreter_api_agent/GuiAgentLoopCore/YamlGuardian/rule_config",
        required=False,
    )

    args = parser.parse_args()

    data = load_yaml_file(args.data)
    yaml_schema = load_validation_rules(args.schema)
    cerberus_schema = convert_yaml_to_cerberus(yaml_schema)
    errors = validate_data(data, cerberus_schema)

    if errors:
        print("Validation failed with the following errors:")
        print(format_errors(errors))
    else:
        print("Validation succeeded.")


if __name__ == "__main__":
    main()
