"""
B-Tree Python implementation
----------------------------
The lecture mentions 2-3 trees which
are a specific form of a more general
data structure called a B-tree. A red-black
tree is also equivalent to a specific type
of B tree.

Below is a example of the general B-tree
data structure

This implementation is based on the example here:
https://www.geeksforgeeks.org/b-tree-set-1-introduction-2/

"""


class BTreeNode(object):
  """
  B-tree node initialized with a list to keep track of keys,
  some comparable type, let's say ints and a list for children
  which will contain other B-tree nodes

  """
  def __init__(self, t): # minimum degree t
    self.t = t
    self.max_capacity = (2 * t) - 1
    self.keys = []
    self.children = []
    self.parent = None

  def is_leaf(self):
    """
    Returns true if the node is a leaf node

    """
    return len(self.children) == 0

  def insert(self, key):
    """
    Insert a node into the tree, assuming the current node
    is the current root. Returns the new root of the tree

    """
    n = len(self.keys)
    if n == 0:
      self.keys.append(key)
      return self
    if n == self.max_capacity:
      new_root = BTreeNode(self.t)
      new_root.children.append(self)
      new_root._split_child(self, 0)
      i = 0
      if new_root.keys[0] < key:
        i += 1
      new_root.children[i]._insert_non_full(key)
      return new_root
    self._insert_non_full(key)
    return self

  def _insert_non_full(self, key):
    """
    This is an auxilary function for the .insert()
    method above. It inserts a key into a node with
    less than (2 * t) - 1 keys

    """
    n = len(self.keys)
    i = n - 1
    while i >= 0 and self.keys[i] > key:
        i -= 1
    if self.is_leaf():
      # if it's a leaf node, insert the new key into the keys list
      self.keys = self.keys[:i + 1] + [key] + self.keys[i + 1:]
    else:
      # Otherwise insert it into the proper child
      child = self.children[i + 1]
      if len(child.keys) == self.max_capacity:
        self._split_child(child, i + 1)
      if i != n - 1 and self.keys[i + 1] < key:
        i += 1
      child._insert_non_full(key)

  def _split_child(self, child, i):
    """
    Split one of the node's children into two,
    each with (t - 1) and t children

    """
    n = len(self.keys)
    new_node = BTreeNode(self.t)

    for k in range(self.t - 1):
      new_node.keys.append(child.keys.pop())
    new_node.keys.reverse()

    if not child.is_leaf():
      for k in range(self.t):
        new_node.children.append(child.children.pop())
    new_node.children.reverse()

    self.children = \
      self.children[:i + 1] + [new_node] + self.children[i + 1:]

    self.keys = self.keys[:i] + [child.keys.pop()] + self.keys[i:]

