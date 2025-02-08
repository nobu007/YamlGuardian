from yamlguardian.rules import RuleManager
from yamlguardian.validate import format_errors, validate_data


class YamlGuardian:
    def __init__(self, schema_file, relations_file=None, common_definitions_file=None):
        self.schema = self.load_yaml_schema(schema_file)
        self.relations = self.load_yaml(relations_file) if relations_file else None
        self.common_definitions = self.load_yaml(common_definitions_file) if common_definitions_file else None
        self.rule_manager = RuleManager(self.schema, self.relations, self.common_definitions)

    def validate(self, data):
        errors = validate_data(data, self.schema)
        if errors:
            return format_errors(errors)
        return self.rule_manager.validate(data)
