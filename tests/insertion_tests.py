from bplus_tree import BPlusTree

# Second Test - Testing the insertion methods

# 1) Simple insertions

print("--- Testing Simple Insertion ---")

tree = BPlusTree(3)

tree.insert(10, "Tom")
tree.insert(20, "Morgan")

print(f"{tree.search_value(10)}")  # Should return Tom
print(f"{tree.search_value(20)}")  # Should return Morgan
print(tree)

# 2) First split test

print("\n--- First split test ---")

tree.insert(15, "Robert")

print(f"{tree.search_value(15)}")  # Should return Robert
print(f"{tree.search(10)}")
print(f"{tree.search(15)}")
print(f"{tree.search(20)}")
print(tree)


# 3) Second split test

print("\n--- Second split test ---")

tree.insert(8, "Michael")
tree.insert(9, "Hailee")
tree.insert(11, "Jaden")
tree.insert(12, "Matthew")

tree.visualization()
print(tree)

# 4) Testing overwrite

print("\n--- Testing Overwrite ---")

tree.insert(10, "Will")
print(f"{tree.search_value(10)}")  # Should return Will

# 5) Testing doubly linked list

print("\n--- Testing Doubly Linked List ---")

current_leaf = tree.search(8)  # Since 8 is the smallest key in this case
while current_leaf:
    print(f"Leaf: {current_leaf} -> {current_leaf.next_leaf}")
    current_leaf = current_leaf.next_leaf
