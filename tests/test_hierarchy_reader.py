import unittest

import pytest

from yamlguardian.hierarchy_reader import HierarchyReader


class TestHierarchyReader(unittest.TestCase):
    def setUp(self):
        self.reader = HierarchyReader()

    def test_read_hierarchy_valid(self):
        hierarchy = self.reader.read_hierarchy("test_yamls/test_data.yaml")
        assert isinstance(hierarchy, dict)
        assert "name" in hierarchy
        assert "age" in hierarchy

    def test_read_hierarchy_invalid(self):
        with pytest.raises(FileNotFoundError):
            self.reader.read_hierarchy("test_yamls/non_existent.yaml")


if __name__ == "__main__":
    unittest.main()
