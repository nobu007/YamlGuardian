import yaml
from .validator import Validator
from .rules import RuleManager
from .validate import load_yaml_schema, validate_data, format_errors

class YamlGuardian:
    def __init__(self, schema_file, relations_file=None, common_definitions_file=None):
        self.schema = self.load_yaml(schema_file)
        self.relations = self.load_yaml(relations_file) if relations_file else None
        self.common_definitions = self.load_yaml(common_definitions_file) if common_definitions_file else None
        self.rule_manager = RuleManager(self.schema, self.relations, self.common_definitions)

    def load_yaml(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def validate(self, data):
        schema = load_yaml_schema(self.schema)
        errors = validate_data(data, schema)
        if errors:
            return format_errors(errors)
        return self.rule_manager.validate(data)
