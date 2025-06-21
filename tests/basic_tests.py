import unittest
from bplus_tree import BPlusTree

# To test it, run python3 -m tests.basic_tests.py

# Fifth Test - Testing all the features


class TestBPlusTree(unittest.TestCase):
    def setUp(self):
        self.tree = BPlusTree(4)  # Small order for easy testing

    def test_single_insertion(self):
        self.tree.insert(10, "a")
        self.assertEqual(self.tree.search_value(10), "a")

    def test_multiple_insertions(self):
        for key, value in [(5, "a"), (15, "b"), (25, "c")]:
            self.tree.insert(key, value)
        self.assertEqual(self.tree.search_value(5), "a")
        self.assertEqual(self.tree.search_value(15), "b")
        self.assertEqual(self.tree.search_value(25), "c")

    def test_overwrite_key(self):
        self.tree.insert(10, "a")
        self.tree.insert(10, "b")  # Should overwrite
        self.assertEqual(self.tree.search_value(10), "b")

    def test_key_not_found(self):
        self.tree.insert(20, "x")
        self.assertIsNone(self.tree.search_value(99))  # Key doesn't exist

    def test_range_query(self):
        self.assertTrue(
            hasattr(self.tree, "range_query"),
            "BPlusTree must implement range_query method.",
        )
        for i in range(1, 10):
            self.tree.insert(i, f"v{i}")
        results = self.tree.range_query(3, 7)
        expected = [(i, f"v{i}") for i in range(3, 8)]
        self.assertEqual(results, expected)

    def test_leaf_node_ordering(self):
        self.assertTrue(
            hasattr(self.tree, "get_all_leaf_keys"),
            "BPlusTree must implement get_all_leaf_keys method.",
        )
        for i in [20, 5, 15, 10]:
            self.tree.insert(i, str(i))
        leaves = self.tree.get_all_leaf_keys()
        self.assertEqual(leaves, sorted(leaves))

    def test_split_propagation(self):
        for i in range(100):
            self.tree.insert(i, str(i))
        for i in range(100):
            with self.subTest(i=i):
                self.assertEqual(self.tree.search_value(i), str(i))

    def test_edge_case_keys(self):
        edge_keys = [-1000, 0, 999999]
        for k in edge_keys:
            self.tree.insert(k, str(k))
        for k in edge_keys:
            with self.subTest(k=k):
                self.assertEqual(self.tree.search_value(k), str(k))

    def test_duplicate_insertion(self):
        self.tree.insert(1, "a")
        self.tree.insert(1, "b")  # Expected to overwrite
        self.assertEqual(self.tree.search_value(1), "b")

    def test_deletion(self):
        # Only run this test if delete is implemented
        if hasattr(self.tree, "delete"):
            self.tree.insert(10, "a")
            self.tree.delete(10)
            self.assertIsNone(self.tree.search_value(10))
        else:
            self.skipTest("Delete method not implemented in BPlusTree")


if __name__ == "__main__":
    unittest.main()
