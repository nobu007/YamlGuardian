class HierarchyMerger:
    def merge_hierarchies(self, hierarchies):
        merged_hierarchy = {}
        for hierarchy in hierarchies:
            self._merge_dicts(merged_hierarchy, hierarchy)
        return merged_hierarchy

    def _merge_dicts(self, dict1, dict2):
        for key, value in dict2.items():
            if key in dict1:
                if isinstance(dict1[key], dict) and isinstance(value, dict):
                    self._merge_dicts(dict1[key], value)
                elif isinstance(dict1[key], list) and isinstance(value, list):
                    dict1[key].extend(value)
                else:
                    dict1[key] = value
            else:
                dict1[key] = value
