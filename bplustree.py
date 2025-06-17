# Some important considerations about B+ Trees:
# Internal nodes only store keys to guide the search;
# Only the leaf nodes store data and are also linked together through a linked list (in this project, it was implemented using a doubly-linked list);
# All leaf nodes must be at the same level, ensuring that the B+ Tree is always balanced;
# The order specifies the maximum number of children a node can have;
# A leaf node in a B+ Tree of order (m) can hold a maximum of (m - 1) keys.


class LeafNode:
    """
    Represents a leaf node that stores real data values;
    They are also connected with a doubly-linked list for efficient range queries;
    The m param is the order.
    """

    def __init__(self, m):
        self.keys = []
        self.values = []
        self.next_leaf = None  # Pointers to the next leaf in the linked list
        self.prev_leaf = None  # Pointers to the previous leaf in the linked list
        self.parent = None
        self.m = m

    def is_full(self):
        # A leaf node is full if it has (m - 1) keys
        return len(self.keys) == self.m - 1

    def is_empty(self):
        return len(self.keys) == 0


class InternalNode:
    """
    Represents an internal node that only stores keys for navigation;
    Internal nodes guide the search path to the appropriate leaf nodes;
    The m param is the order.
    """

    def __init__(self, m):
        self.keys = []
        self.children = []  # Pointers to child nodes
        self.parent = None  # Pointers to the parent node, useful for rebalancing
        self.m = m

    def is_full(self):
        # A leaf node is full if it has (m - 1) keys
        return len(self.keys) == self.m - 1

    def is_empty(self):
        return len(self.keys) == 0


class BPlusTree:
    """
    B+ tree data structure optimized for database and file system applications.
    Provides efficient insertion, deletion, and range query operations.
    """

    def __init__(self, m):
        self.m = m
        self.root = LeafNode(m)
