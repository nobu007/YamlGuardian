import csv
import os
import time

import pandas as pd
import yaml

from .hierarchy_merger import HierarchyMerger
from .hierarchy_reader import HierarchyReader


class DirectoryAnalyzer:
    cache_file = "cache.csv"

    def __init__(self, cache_file=None):
        self.cache = {}
        self.cache_file = cache_file or DirectoryAnalyzer.cache_file
        self.load_cache()
        self.hierarchy_reader = HierarchyReader()
        self.hierarchy_merger = HierarchyMerger()

    def load_cache(self):
        if os.path.exists(self.cache_file):
            df = pd.read_csv(self.cache_file)
            for _, row in df.iterrows():
                self.cache[row["Path"]] = (yaml.safe_load(row["Content"]), row["Timestamp"])

    def load_yaml_with_cache(self, file_path):
        if file_path in self.cache:
            cached_content, cached_timestamp = self.cache[file_path]
            current_timestamp = os.path.getmtime(file_path)
            if current_timestamp <= cached_timestamp:
                return cached_content
        with open(file_path, "r", encoding="utf-8") as file:
            content = yaml.safe_load(file)
            self.cache[file_path] = (content, os.path.getmtime(file_path))
            return content

    def analyze_directory_structure(self, root_dir):
        self.load_yaml_with_cache(root_dir)
        hierarchies = []
        changes = []
        for root, dirs, files in os.walk(root_dir):
            for name in files:
                if name.endswith(".yaml"):
                    file_path = os.path.join(root, name)
                    hierarchy = self.read_hierarchy(file_path)
                    hierarchies.append(hierarchy)
                    self.cache[file_path] = (hierarchy, os.path.getmtime(file_path))
                    changes.append(["File", file_path])
            for name in dirs:
                changes.append(["Directory", os.path.join(root, name)])
        merged_hierarchy = self.merge_hierarchies(hierarchies)
        return changes

    def save_cache(self):
        data = []
        for path, (content, timestamp) in self.cache.items():
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
