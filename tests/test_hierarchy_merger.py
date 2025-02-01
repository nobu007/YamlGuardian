import unittest
from yamlguardian.hierarchy_merger import HierarchyMerger

class TestHierarchyMerger(unittest.TestCase):

    def setUp(self):
        self.merger = HierarchyMerger()

    def test_merge_hierarchies_simple(self):
        hierarchies = [
            {'name': 'John', 'age': 30},
            {'city': 'New York', 'country': 'USA'}
        ]
        merged = self.merger.merge_hierarchies(hierarchies)
        self.assertEqual(merged['name'], 'John')
        self.assertEqual(merged['age'], 30)
        self.assertEqual(merged['city'], 'New York')
        self.assertEqual(merged['country'], 'USA')

    def test_merge_hierarchies_nested(self):
        hierarchies = [
            {'person': {'name': 'John', 'age': 30}},
            {'person': {'address': {'city': 'New York', 'country': 'USA'}}}
        ]
        merged = self.merger.merge_hierarchies(hierarchies)
        self.assertEqual(merged['person']['name'], 'John')
        self.assertEqual(merged['person']['age'], 30)
        self.assertEqual(merged['person']['address']['city'], 'New York')
        self.assertEqual(merged['person']['address']['country'], 'USA')

    def test_merge_hierarchies_conflict(self):
        hierarchies = [
            {'name': 'John', 'age': 30},
            {'name': 'Jane', 'age': 25}
        ]
        merged = self.merger.merge_hierarchies(hierarchies)
        self.assertEqual(merged['name'], 'Jane')
        self.assertEqual(merged['age'], 25)

if __name__ == '__main__':
    unittest.main()
