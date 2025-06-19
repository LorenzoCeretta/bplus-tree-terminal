from bplus_tree import BPlusTree, LeafNode, InternalNode

# Implementing a B+ Tree without the insertion method, to test the classes and the search

# Bulding the following B+ Tree, of order m = 3:

#       [ 10 ,  20 ]  Root
#       /    |     \
#      /     |      \
# [2,8]<->[10,15]<->[20,30]  Leaf Nodes

m = 3  # Order

# First Node
leaf1 = LeafNode(m)
leaf1.keys = [2, 8]
leaf1.values = ["Leo", "Brad"]

# Second Node
leaf2 = LeafNode(m)
leaf2.keys = [10, 15]
leaf2.values = ["Chris", "Ben"]

# Third Node
leaf3 = LeafNode(m)
leaf3.keys = [20, 30]
leaf3.values = ["Samuel", "Denzel"]

# Doubly Linked List
leaf1.next_leaf = leaf2
leaf2.prev_leaf = leaf1
leaf2.next_leaf = leaf3
leaf3.prev_leaf = leaf2

# Creating the Root
root = InternalNode(m)
root.keys = [10, 20]
root.children = [leaf1, leaf2, leaf3]

# Pointers
leaf1.parent = root
leaf2.parent = root
leaf3.parent = root

# Initialzing the B+ Tree
tree = BPlusTree(m)
tree.root = root

print("--- Testing Tree ---")
print("Tree --> ", tree)
print("Root --> ", root)
print("Leaf --> ", leaf1)
print("Leaf --> ", leaf2)
print("Leaf --> ", leaf3)

print("\n--- Testing Search Value ---")
print(f"Search (15): {tree.search_value(15)}")  # Should return Ben
print(f"Search (2): {tree.search_value(2)}")  # Should return Leo
print(f"Search (30): {tree.search_value(30)}")  # Should return Denzel
print(f"Search (5): {tree.search_value(5)}")  # Should return None
print(f"Search (25): {tree.search_value(25)}")  # Should return None

print("\n--- Testing Search Leafs ---")
print(f"Search (15): {tree.search(15)}")
print(f"Search (2): {tree.search(2)}")
print(f"Search (30): {tree.search(30)}")
print(f"Search (5): {tree.search(5)}")  # Should return the insertion correct place
print(f"Search (25): {tree.search(25)}")  # Should return the insertion correct place
