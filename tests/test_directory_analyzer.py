import csv
import os
import unittest

from yamlguardian.directory_analyzer import DirectoryAnalyzer


class TestDirectoryAnalyzer(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_directory"
        os.makedirs(self.test_dir, exist_ok=True)
        with open(os.path.join(self.test_dir, "test_file.txt"), "w") as f:
            f.write("test content")
        with open(os.path.join(self.test_dir, "test_file.yaml"), "w") as f:
            f.write("name: test\nage: 30")

    def tearDown(self):
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    def test_analyze_directory_structure(self):
        analyzer = DirectoryAnalyzer()
        changes = analyzer.analyze_directory_structure(self.test_dir)
        assert len(changes) == 3
        assert changes[0] == ["Directory", self.test_dir]
        assert changes[1] == ["File", os.path.join(self.test_dir, "test_file.txt")]
        assert changes[2] == ["File", os.path.join(self.test_dir, "test_file.yaml")]

    def test_save_changes_to_csv(self):
        analyzer = DirectoryAnalyzer()
        changes = analyzer.analyze_directory_structure(self.test_dir)
        csv_file = "test_directory_structure_changes.csv"
        analyzer.save_changes_to_csv(changes, csv_file)
        with open(csv_file) as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) == 4
            assert rows[0] == ["Type", "Path"]
            assert rows[1] == ["Directory", self.test_dir]
            assert rows[2] == ["File", os.path.join(self.test_dir, "test_file.txt")]
            assert rows[3] == ["File", os.path.join(self.test_dir, "test_file.yaml")]
        os.remove(csv_file)

    def test_load_yaml_with_cache(self):
        analyzer = DirectoryAnalyzer()
        file_path = os.path.join(self.test_dir, "test_file.yaml")
        content1 = analyzer.load_yaml_with_cache(file_path)
        content2 = analyzer.load_yaml_with_cache(file_path)
        assert content1 == content2
        assert file_path in analyzer.validation_schema_cache


if __name__ == "__main__":
    unittest.main()
