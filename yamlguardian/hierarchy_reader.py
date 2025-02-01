import yaml

class HierarchyReader:
    def read_hierarchy(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            hierarchy = yaml.safe_load(file)
        return hierarchy
