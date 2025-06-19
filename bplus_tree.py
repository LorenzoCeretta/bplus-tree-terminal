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
        self.parent = None  # Pointers to the parent node, useful for rebalancing
        self.m = m

    def is_full(self):
        # A leaf node is full if it has (m - 1) keys
        return len(self.keys) == self.m - 1

    def is_empty(self):
        return len(self.keys) == 0

    def __str__(self):
        return f"LeafNode(keys={self.keys}, values={self.values})"


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

    def __str__(self):
        return f"InternalNode(keys={self.keys}, children_count={len(self.children)})"


class BPlusTree:
    """
    B+ tree class to manage all the operations.
    """

    def __init__(self, m):
        self.m = m
        self.root = LeafNode(m)

    def __str__(self):
        return f"BPlusTree(order={self.m}, root={self.root})"

    def search(self, key):
        """
        Traverses down from the root through internal nodes using key comparisons
        to guide the path, then searches within the target leaf node for the key.
        """

        current_node = self.root

        # Navigate in a transversal way trough nodes until reach a leaf
        while isinstance(
            current_node, InternalNode
        ):  # isinstance is a python function to check if an object is from a specified class or a subclass from it

            node_keys = current_node.keys
            child_index = 0

            # Find the correct child to follow
            for i in range(len(node_keys)):
                if key < node_keys[i]:
                    child_index = i
                    break
                else:
                    child_index = i + 1

            # Move to the correct child
            current_node = current_node.children[child_index]

        if isinstance(
            current_node, LeafNode
        ):  # Now at the leaf layer, search for the appropriate key
            for i in range(len(current_node.keys)):
                if current_node.keys[i] == key:
                    return current_node.values[i]

        # If key not found
        print(f"Key {key} not found in search")
        return None
