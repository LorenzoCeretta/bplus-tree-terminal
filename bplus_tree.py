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
        self.next_leaf = None  # Pointers to the next leaf
        self.prev_leaf = None  # Pointers to the previous
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
        # An internal node is full if it has (m - 1) keys
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
        Navigates down from the root through internal nodes to find the leaf node
        where the key is located or should be inserted.

        Returns:
            LeafNode: The leaf node that either:
                     - Contains the key (if key exists)
                     - Should contain the key (if key doesn't exist) -useful for insertion

        Note:
            Use search_value() to check if a key actually exists in the tree.
        """
        current_node = self.root

        # Navigate trough nodes until reach a leaf
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

        return current_node

    def search_value(self, key):
        """
        Search for a specific value using the search() function to find the proper leaf node.
        """
        leaf = self.search(key)

        # Search the value inside the leaf node
        for i in range(len(leaf.keys)):
            if leaf.keys[i] == key:
                return leaf.values[i]

        # If key not found
        return None

    def insert(self, key, value):
        """
        Handle insertions of a key-value pair into the B+ tree.
        """
        # Step 1 - find which leaf to insert
        leaf = self.search(key)

        # Step 2 - insert in the leaf, keeping the order
        self.insert_at_leaf(leaf, key, value)

        # Step 3 - check if split is necessary (overflow)
        if len(leaf.keys) == self.m:

            new_leaf = LeafNode(self.m)

            mid = len(leaf.keys) // 2  # Calculate split point

            # Move half the keys/values to new leaf
            new_leaf.keys = leaf.keys[mid:]
            new_leaf.values = leaf.values[mid:]
            new_leaf.parent = leaf.parent

            # Update original leaf
            leaf.keys = leaf.keys[:mid]
            leaf.values = leaf.values[:mid]

            # Update leaf links
            new_leaf.next_leaf = leaf.next_leaf
            new_leaf.prev_leaf = leaf
            if leaf.next_leaf:
                leaf.next_leaf.prev_leaf = new_leaf
            leaf.next_leaf = new_leaf

            # Insert in parent
            self.insert_in_parent(leaf, new_leaf.keys[0], new_leaf)

    def insert_at_leaf(self, leaf, key, value):
        """
        Inserts a key-value pair into leaf node keeping the order.
        """
        if leaf.keys:  # Non-empty leaf
            for i in range(len(leaf.keys)):
                if key == leaf.keys[i]:
                    leaf.values[i] = value  # Overwrite existing value
                    return
                elif key < leaf.keys[i]:
                    leaf.keys.insert(i, key)  # Insert the key in the correct position
                    leaf.values.insert(
                        i, value
                    )  # Insert the value in the correct position
                    return

            # If the key is greater than the others, append it
            leaf.keys.append(key)
            leaf.values.append(value)

        else:  # Empty leaf
            leaf.keys = [key]
            leaf.values = [value]

    def insert_in_parent(self, original_node, key, new_right_node):
        """
        Handles both leaf and internal node splits.
        """
        # Case 1: original_node is root
        if original_node.parent is None:
            new_root = InternalNode(self.m)
            new_root.keys = [key]
            new_root.children = [original_node, new_right_node]
            self.root = new_root
            original_node.parent = new_root
            new_right_node.parent = new_root
            return

        # Case 2: Insert into parent
        parent = original_node.parent
        new_right_node.parent = parent

        # Find position and insert
        for i in range(len(parent.children)):
            if parent.children[i] == original_node:
                parent.keys.insert(i, key)
                parent.children.insert(i + 1, new_right_node)
                break

        # Case 3: Parent overflow
        if len(parent.keys) == self.m:

            new_parent = InternalNode(self.m)
            new_parent.parent = parent.parent

            mid = len(parent.keys) // 2  # Split point
            promoted_key = parent.keys[mid]

            # Move keys and children
            new_parent.keys = parent.keys[mid + 1 :]
            new_parent.children = parent.children[mid + 1 :]

            # Update original parent
            parent.keys = parent.keys[:mid]
            parent.children = parent.children[: mid + 1]

            # Update children's parent pointers
            for child in new_parent.children:
                child.parent = new_parent

            # Recursive call to handle parent split
            self.insert_in_parent(parent, promoted_key, new_parent)
