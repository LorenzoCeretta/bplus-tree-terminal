from bplus_tree import BPlusTree

# To test it, run python3 -m tests.delete_tests

# Third Test - Testing the delete methods

# 0) Set-up

print("--- Initializing B+ Tree ---\n")

tree = BPlusTree(4)  # order m = 4

keys = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 7, 18]

for k in keys:
    tree.insert(k, str(k))

tree.visualization()

# 1) Simple delete - delete from a leaf that has more than minimum keys

tree_test1 = tree
print("\n----- Test 1 -----")
print(" Delete(7) -> causing Simple Delete. Result:\n")
tree_test1.delete(7)
tree_test1.visualization()

# 2) Delete that triggers borrow from right sibling (leaf level only)

print("\n----- Test 2 -----")
print("Delete(5) -> causing Borrow. Result:\n")
tree.delete(5)
tree.visualization()

# 3) Delete that triggers merge with sibling

print("\n----- Test 3 -----")
print("Delete(15) -> causing Merge. Result:\n")
tree.delete(15)
tree.visualization()

# 4) Delete that causes tree to shrink one level
print("\n----- Test 4 -----")
print(" Delete(20), Delete(25) -> causing tree shrink. Result:\n")
tree.delete(20)
tree.delete(25)
tree.visualization()
