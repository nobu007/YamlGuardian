class Validator:
    def __init__(self, schema):
        self.schema = schema

    def validate(self, data):
        errors = []
        for element in self.schema.get('root_element', []):
            if element.get('required') and element['name'] not in data:
                errors.append(f"{element['description']} が存在しません。")
            if element.get('type') == 'string':
                if not isinstance(data.get(element['name']), str):
                    errors.append(f"{element['description']} は文字列である必要があります。")
            elif element.get('type') == 'integer':
                if not isinstance(data.get(element['name']), int):
                    errors.append(f"{element['description']} は整数である必要があります。")
            # Add more type checks as needed
        return errors
