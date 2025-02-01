import yaml

def convert_yaml_to_cerberus(yaml_schema):
    cerberus_schema = {}
    for field, rules in yaml_schema.items():
        cerberus_rules = {}
        for rule, value in rules.items():
            if rule == 'type':
                cerberus_rules['type'] = value
            elif rule == 'minlength':
                cerberus_rules['minlength'] = value
            elif rule == 'maxlength':
                cerberus_rules['maxlength'] = value
            elif rule == 'required':
                cerberus_rules['required'] = value
            # Add more mappings as needed
        cerberus_schema[field] = cerberus_rules
    return cerberus_schema

def load_yaml_file(file_path):
    with open(file_path, 'r') as file:
        yaml_content = yaml.safe_load(file)
    return yaml_content
