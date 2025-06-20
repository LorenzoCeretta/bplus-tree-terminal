from bplus_tree import BPlusTree, LeafNode, InternalNode

# Second Test - Testing the insertion methods

# 1) Simple insertions

print("--- Testing Simple Insertion ---")

tree = BPlusTree(3)

tree.insert(10, "Tom")
tree.insert(20, "Morgan")

print(f"{tree.search_value(10)}")  # Should return Tom
print(f"{tree.search_value(20)}")  # Should return Morgan
print(tree)

# 2) Testing first split

print("\n--- Testing First Split ---")

tree.insert(15, "Robert")

print(f"{tree.search_value(15)}")  # Should return Robert
print(f"{tree.search(10)}")
print(f"{tree.search(15)}")
print(f"{tree.search(20)}")
print(tree)


# 3) Testing second split

print("\n--- Testing Second Split ---")

tree.insert(8, "Michael")
tree.insert(9, "Hailee")
tree.insert(11, "Jaden")
tree.insert(12, "Matthew")

print(f"{tree.search(8)}")
print(f"{tree.search(9)}")
print(f"{tree.search(10)}")
print(f"{tree.search(11)}")
print(f"{tree.search(12)}")
print(f"{tree.search(15)}")
print(f"{tree.search(20)}")

print(tree)

# 4) Testing overwrite

print("\n--- Testing Overwrite ---")

tree.insert(10, "Will")
print(f"{tree.search_value(10)}")  # Should return Will
