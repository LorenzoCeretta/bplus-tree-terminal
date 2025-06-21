from bplus_tree import BPlusTree

# To test it, run python3 -m tests.utilities_tests

# Fourth Test - Testing the utilities

# 0) Set-up

print("--- Initializing B+ Tree ---\n")

tree = BPlusTree(3)

keys = [0, 1, 2, 4, 8, 16]
value = ["Ted", "Robin", "Barney", "Marshall", "Lily", "Victoria"]

for k, v in zip(keys, value):
    tree.insert(k, v)

tree.visualization()

# 1) Range Query - Return all key-value pairs in the range [start, end]

print("--- Test 1 - Range Query ---\n")

print(
    tree.range_query(2, 8)
)  # Should return list of tuples: [(2, 'Barney'), (4, 'Marshall'), (8, 'Lily')]

# 2) Get All Leaf Keys  - Return all keys in the tree in sorted order.

print("--- Test 2 - Get All Leaf Keys ---\n")

print(tree.get_all_leaf_keys())  # Should return [0, 1, 2, 4, 8, 16]
