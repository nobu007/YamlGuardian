class Validator:
    def __init__(self, schema):
        self.schema = schema

    def validate(self, data):
        errors = []
        for element in self.schema.get("root_element", []):
            if element.get("required") and element["name"] not in data:
                errors.append(f"{element['description']} が存在しません。")
            if element.get("type") == "string":
                if not isinstance(data.get(element["name"]), str):
                    errors.append(f"{element['description']} は文字列である必要があります。")
            elif element.get("type") == "integer":
                if not isinstance(data.get(element["name"]), int):
                    errors.append(f"{element['description']} は整数である必要があります。")
            elif element.get("type") == "list":
                if not isinstance(data.get(element["name"]), list):
                    errors.append(f"{element['description']} はリストである必要があります。")
            elif element.get("type") == "object":
                if not isinstance(data.get(element["name"]), dict):
                    errors.append(f"{element['description']} はオブジェクトである必要があります。")
            # Add more type checks as needed

            # Custom validation rules
            if "custom_rules" in element:
                for rule in element["custom_rules"]:
                    if not rule(data.get(element["name"])):
                        errors.append(f"{element['description']} のカスタムルールに違反しています。")

            # Check for uses_common attribute
            if element.get("uses_common"):
                common_element = next(
                    (e for e in self.common_definitions.get("common_elements", []) if e["name"] == element["name"]),
                    None,
                )
                if not common_element:
                    errors.append(f"{element['description']} は共通要素として定義されていません。")

            # Check for required fields
            if element.get("required") and element["name"] not in data:
                errors.append(f"{element['description']} が存在しません。")

            # Check for prohibited fields
            if element.get("prohibited") and element["name"] in data:
                errors.append(f"{element['description']} は選択できません。")

        return errors
