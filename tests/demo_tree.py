from bplus_tree import BPlusTree, LeafNode, InternalNode

# Implementing the B+ Tree without the insertion method, to build the search method first

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

print(tree)
