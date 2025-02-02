import os
import yaml
import time
import pandas as pd
import csv
from .hierarchy_reader import HierarchyReader
from .hierarchy_merger import HierarchyMerger


class DirectoryAnalyzer:
    cache_file = "cache.csv"

    def __init__(self, cache_file=None):
        self.validation_rules = {}
        self.validation_schema = {}
        self.validation_schema_cache = {}
        self.cache_file = cache_file or DirectoryAnalyzer.cache_file
        self.load_cache()
        self.hierarchy_reader = HierarchyReader()
        self.hierarchy_merger = HierarchyMerger()

    def load_cache(self):
        if os.path.exists(self.cache_file):
            df = pd.read_csv(self.cache_file)
            for _, row in df.iterrows():
                self.validation_schema_cache[row["Path"]] = (yaml.safe_load(row["Content"]), row["Timestamp"])

    def load_yaml_with_cache(self, file_path) -> tuple[dict, bool]:
        is_changed = False
        if file_path in self.validation_schema_cache:
            cached_content, cached_timestamp = self.validation_schema_cache[file_path]
            current_timestamp = os.path.getmtime(file_path)
            if current_timestamp <= cached_timestamp:
                return cached_content, is_changed

        # read new content
        is_changed = True
        with open(file_path, "r", encoding="utf-8") as file:
            content = yaml.safe_load(file)
            self.validation_schema_cache[file_path] = (content, os.path.getmtime(file_path))
            return content, is_changed

    def analyze_directory_structure(self, root_dir):
        hierarchies = []
        changes = []
        for root, dirs, files in os.walk(root_dir):
            for name in files:
                if name.endswith(".yaml"):
                    # load
                    full_path = os.path.abspath(os.path.join(root, name))
                    validation_rule, is_changed = self.load_yaml_with_cache(full_path)
                    if validation_rule:
                        self.validation_rules[full_path] = validation_rule
                    else:
                        print(f"Failed to load {full_path}")

                    # TODO: analyze hierarchy
                    # hierarchy = self.read_hierarchy(file_path)
                    # hierarchies.append(hierarchy)

                    # changes
                    if is_changed:
                        changes.append(["File", full_path])
                        change_dir = os.path.dirname(full_path)
                        if not any(x[1] == change_dir for x in changes):
                            changes.append(["Directory", change_dir])

        # TODO: analyze hierarchy
        # merged_hierarchy = self.merge_hierarchies(hierarchies)

        # use full cache
        if len(changes) == 0:
            self.validation_schema = self.validation_schema_cache
            return changes

        # temp
        self.validation_schema = self.validation_rules
        return self.validation_schema

    def save_cache(self):
        data = []
        for path, (content, timestamp) in self.validation_schema_cache.items():
            data.append({"Path": path, "Content": yaml.dump(content), "Timestamp": timestamp})
        df = pd.DataFrame(data)
        df.to_csv(self.cache_file, index=False)

    def save_changes_to_csv(self, changes, csv_file):
        with open(csv_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Type", "Path"])
            writer.writerows(changes)

    def read_hierarchy(self, file_path):
        return self.hierarchy_reader.read_hierarchy(file_path)

    def merge_hierarchies(self, hierarchies):
        return self.hierarchy_merger.merge_hierarchies(hierarchies)


if __name__ == "__main__":
    analyzer = DirectoryAnalyzer()
    root_directory = "."
    changes = analyzer.analyze_directory_structure(root_directory)

    analyzer.save_changes_to_csv(changes, "directory_structure_changes.csv")
    analyzer.save_cache()
    print(f"Changes saved to directory_structure_changes.csv")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
