# Some important considerations about B+ Trees:
# Leaf nodes store data and are linked together trough a linked list;
# Internal nodes only store keys to guide the search;
# A leaf node in a B+ Tree or order (m) can hold a maximum of (m - 1) keys.

class LeafNode:
  def __init__(self):
    self.data = []
    self.next_leaf = None
    self.prev_leaf = None

  def is_full(self, m):
    # m means the order of the B+ tree
    # A leaf node is full if it has (m - 1) keys
    return len(self.keys) == m - 1

  def is_empty(self):
    return len(self.keys) == 0

class InternalNode:
  def __init__(self):
    self.children = [] # Pointers to child notes

  def is_full(self, m):
    return len(self.keys) == m -1

  def is_empty(self):
    return len(self.keys) == 0

class BPlusTree:
  def __init__(self, m):
    self.root = LeafNode()
    self.m = m 