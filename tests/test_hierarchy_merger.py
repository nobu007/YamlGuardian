import unittest

from yamlguardian.hierarchy_merger import HierarchyMerger


class TestHierarchyMerger(unittest.TestCase):
    def setUp(self):
        self.merger = HierarchyMerger()

    def test_merge_hierarchies_simple(self):
        hierarchies = [{"name": "John", "age": 30}, {"city": "New York", "country": "USA"}]
        merged = self.merger.merge_hierarchies(hierarchies)
        assert merged["name"] == "John"
        assert merged["age"] == 30
        assert merged["city"] == "New York"
        assert merged["country"] == "USA"

    def test_merge_hierarchies_nested(self):
        hierarchies = [
            {"person": {"name": "John", "age": 30}},
            {"person": {"address": {"city": "New York", "country": "USA"}}},
        ]
        merged = self.merger.merge_hierarchies(hierarchies)
        assert merged["person"]["name"] == "John"
        assert merged["person"]["age"] == 30
        assert merged["person"]["address"]["city"] == "New York"
        assert merged["person"]["address"]["country"] == "USA"

    def test_merge_hierarchies_conflict(self):
        hierarchies = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]
        merged = self.merger.merge_hierarchies(hierarchies)
        assert merged["name"] == "Jane"
        assert merged["age"] == 25


if __name__ == "__main__":
    unittest.main()
