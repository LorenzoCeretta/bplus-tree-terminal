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

    # ----- Search Method and Search Helpers -----

    def search(self, key):
        """
        Navigates down from the root through internal nodes to find the leaf node
        where the key is located or should be inserted.

        Returns:
            LeafNode: The leaf node that either:
                     - Contains the key (if key exists)
                     - Should contain the key (if key doesn't exist) - useful for insertion

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

    def visualization(self):
        """
        Function made by AI to help with the tree visualization
        """

        def _fmt(keys):
            return ",".join(map(str, keys))

        def _walk(node, depth=0) -> str:
            indent = "  " * depth
            if isinstance(node, LeafNode):
                return f"{indent}[{_fmt(node.keys)}]\n"
            else:
                out = f"{indent}<{_fmt(node.keys)}>\n"
                for child in node.children:
                    out += _walk(child, depth + 1)
                return out

        if self.root is None:
            print("<empty>")
        else:
            print(_walk(self.root), end="")

    # ----- Insert Method and Insert Helpers -----

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

    # ----- Delete Method and Delete Helpers -----

    def delete(self, key):
        """
        Removes the given key and its value from the B+-Tree.
        If the key is not present returns None
        """
        leaf = self.search(key)
        if key not in leaf.keys:
            return None

        idx = leaf.keys.index(key)
        leaf.keys.pop(idx)
        leaf.values.pop(idx)

        if leaf is self.root:  # If root is a leaf node, process finished
            return

        # If the leaf still holds enough keys, only need to fix the separator
        if len(leaf.keys) >= self.minimum_leaf_keys():
            self.fix_parent_key(leaf)
            return

        # Otherwise start the rebalancing process
        self.delete_entry(leaf)

    # Minimum key helpers
    def minimum_leaf_keys(self):
        """(m-1)/2) -> least number of keys a leaf may hold after deletion"""
        return self.m // 2

    def minimum_internal_keys(self):
        """((m/2) − 1) –> least number of keys an internal node may hold"""
        return (self.m - 1) // 2

    def minimum_keys(self, node):
        """Return the allowed minimum for the given node type"""
        return (
            self.minimum_leaf_keys()
            if isinstance(node, LeafNode)
            else self.minimum_internal_keys()
        )

    # Rebalancing
    def delete_entry(self, node):
        parent = node.parent

        # Case 1 – node is root
        if parent is None:
            if isinstance(node, InternalNode) and len(node.children) == 1:
                self.root = node.children[0]
                self.root.parent = None
            return

        # Identify siblings and separator index
        pos = parent.children.index(node)
        left = parent.children[pos - 1] if pos > 0 else None
        right = parent.children[pos + 1] if pos < len(parent.children) - 1 else None

        # 1) Borrow from left
        if left and len(left.keys) > self.minimum_keys(left):
            self.borrow_from_left(node, left, parent, pos - 1)
            return

        # 2) Borrow from right
        if right and len(right.keys) > self.minimum_keys(right):
            self.borrow_from_right(node, right, parent, pos)
            return

        # 3) Merge with a sibling
        if left:
            self.merge_nodes(left, node, parent, pos - 1)
            affected_parent = parent
        else:
            self.merge_nodes(node, right, parent, pos)
            affected_parent = parent

        # Parent may now be deficient
        if affected_parent is self.root and len(affected_parent.keys) == 0:
            self.root = affected_parent.children[0]
            self.root.parent = None
        elif len(affected_parent.keys) < self.minimum_internal_keys():
            self.delete_entry(affected_parent)

    # Rebalancing Utilities
    def fix_parent_key(self, node):
        """Update parent separator when the first key in a leaf changes."""
        parent = node.parent
        if not parent or not node.keys:
            return

        # Find position of this node in parent's children
        pos = parent.children.index(node)

        # If this is not the leftmost child, update the separator key
        if pos > 0:
            parent.keys[pos - 1] = node.keys[0]
            # Recursively fix parent if it's also not the leftmost
            self.fix_parent_key(parent)

    def borrow_from_left(self, node, left, parent, sep_idx):
        """Move one key from the left sibling to node (with parent update)"""
        if isinstance(node, LeafNode):
            node.keys.insert(0, left.keys.pop(-1))
            node.values.insert(0, left.values.pop(-1))
            parent.keys[sep_idx] = node.keys[0]
        else:
            sep_key = parent.keys[sep_idx]
            child = left.children.pop(-1)
            node.children.insert(0, child)
            child.parent = node
            node.keys.insert(0, sep_key)
            parent.keys[sep_idx] = left.keys.pop(-1)

    def borrow_from_right(self, node, right, parent, sep_idx):
        """Move one key from the right sibling to node (with parent update)"""
        if isinstance(node, LeafNode):
            node.keys.append(right.keys.pop(0))
            node.values.append(right.values.pop(0))
            parent.keys[sep_idx] = right.keys[0]
        else:
            sep_key = parent.keys[sep_idx]
            child = right.children.pop(0)
            node.children.append(child)
            child.parent = node
            node.keys.append(sep_key)
            parent.keys[sep_idx] = right.keys.pop(0)

    def merge_nodes(self, left, right, parent, sep_idx):
        """
        Merge two siblings and remove the separator from the parent.
        After the call only the left node survives.
        """
        if isinstance(left, LeafNode):
            left.keys.extend(right.keys)
            left.values.extend(right.values)
            left.next_leaf = right.next_leaf
            if right.next_leaf:
                right.next_leaf.prev_leaf = left
        else:
            separator = parent.keys[sep_idx]  # separator - key between the siblings
            left.keys.append(separator)  # bring separator down into left node
            left.keys.extend(right.keys)
            for child in right.children:
                child.parent = left
            left.children.extend(right.children)

        parent.keys.pop(sep_idx)
        parent.children.pop(sep_idx + 1)

    # ----- Utilities -----

    def range_query(self, start, end):
        """
        Return all key-value pairs in the range [start, end]
        """
        result = []

        current_leaf = self.search(start)  # Find the starting leaf

        # Navigate through the doubly linked list and store the keys in range
        while current_leaf:
            for key, value in zip(current_leaf.keys, current_leaf.values):
                if key > end:
                    return result  # Early termination when pass the end

                # Add key to results if it's >= start
                if key >= start:
                    result.append((key, value))

            current_leaf = current_leaf.next_leaf

        return result

    def get_all_leaf_keys(self):
        """
        Return all keys in the tree in sorted order.
        Uses the doubly-linked leaf structure for it.
        """
        keys = []

        # Find the first leaf
        current_leaf = self.root
        while isinstance(current_leaf, InternalNode):
            current_leaf = current_leaf.children[0]  # Always selects the leftmost child

        # Traverse all leaves using the linked list
        while current_leaf:
            for k in current_leaf.keys:
                keys.append(k)
            current_leaf = (
                current_leaf.next_leaf
            )  # Move to next leaf after processing all keys

        return keys
