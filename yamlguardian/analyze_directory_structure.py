import os
import yaml
import time
import pandas as pd
from .hierarchy_reader import HierarchyReader
from .hierarchy_merger import HierarchyMerger

class DirectoryAnalyzer:
    cache_file = 'cache.csv'

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
                self.cache[row['Path']] = (yaml.safe_load(row['Content']), row['Timestamp'])

    def load_yaml_with_cache(self, file_path):
        if file_path in self.cache:
            cached_content, cached_timestamp = self.cache[file_path]
            current_timestamp = os.path.getmtime(file_path)
            if current_timestamp <= cached_timestamp:
                return cached_content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = yaml.safe_load(file)
            self.cache[file_path] = (content, os.path.getmtime(file_path))
            return content

    def analyze_directory_structure(self, root_dir):
        self.load_yaml_with_cache(root_dir)
        changes = []
        for root, dirs, files in os.walk(root_dir):
            for name in dirs:
                changes.append(['Directory', os.path.join(root, name)])
            for name in files:
                if name.endswith('.yaml'):
                    file_path = os.path.join(root, name)
                    self.load_yaml_with_cache(file_path)
                changes.append(['File', os.path.join(root, name)])
        return changes

    def save_cache(self):
        data = []
        for path, (content, timestamp) in self.cache.items():
            data.append({'Path': path, 'Content': yaml.dump(content), 'Timestamp': timestamp})
        df = pd.DataFrame(data)
        df.to_csv(self.cache_file, index=False)

if __name__ == "__main__":
    analyzer = DirectoryAnalyzer()
    root_directory = '.'
    changes = analyzer.analyze_directory_structure(root_directory)
    analyzer.save_cache()
    print(f"Changes saved to {analyzer.cache_file}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
