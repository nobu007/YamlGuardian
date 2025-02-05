from yamlguardian.validator import Validator


class RuleManager:
    def __init__(self, schema, relations=None, common_definitions=None):
        self.schema = schema
        self.relations = relations
        self.common_definitions = common_definitions
        self.validator = Validator(schema)

    def validate(self, data):
        errors = self.validator.validate(data)
        # Add additional validation rules based on schema
        for element in self.schema.get("root_element", []):
            if element.get("type") == "string":
                if not isinstance(data.get(element["name"]), str):
                    errors.append(f"{element['description']} は文字列である必要があります。")
            elif element.get("type") == "integer":
                if not isinstance(data.get(element["name"]), int):
                    errors.append(f"{element['description']} は整数である必要があります。")
            # Add more type checks as needed
        return errors
