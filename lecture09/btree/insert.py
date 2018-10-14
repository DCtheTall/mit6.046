"""
Augmented B-Tree: Insertion
---------------------------
This folder contains an implementation of an augmented B-tree.
For this implementation, the tree only stores data in its leaf
nodes. Each node also has level-set pointers defined here which
access the left and right siblings of each node (or None if they do not exist).
Each node also has a min/max key which store the minimum and maximum values
stored in the node or its children if it's not a leaf.

This implementation is optimized for finger-searching, i.e. finding a particular
value starting at a given node

This program covers methods for each node used for inserting keys

"""


from search import BTreeSearchNode


class BTreeInsertNode(BTreeSearchNode):
  """
  Augmented B-tree node where only the leaf
  nodes have keys and non-leaf nodes have children

  Each node has a pointer to its min, max elements
  and its left and right siblings

  """
  def __init__(self, t):
    BTreeSearchNode.__init__(self, t)

  def _create_new(self):
    """
    Create a new instance of the node

    """
    return BTreeInsertNode(self.t)

  def _insert_non_full(self, key):
    """
    Insert a new key into a node that is not full

    If the node is a leaf, it will add the key to its list of keys

    If the node is not a leaf, it will insert the key into the proper child

    """
    if self.min is None or key < self.min:
      self.min = key
    if self.max is None or key > self.max:
      self.max = key

    i = self.n - 1
    while i >= 0 and (
      (self.is_leaf() and self.keys[i] > key) or \
        (not self.is_leaf() and self.children[i].min > key)):
          i -= 1
    if self.is_leaf():
      self.keys = self.keys[:i + 1] + [key] + self.keys[i + 1:]
    else:
      child = self.children[i]
      if child.n == child.max_capacity:
        self._split_child(child, i)
        if self.children[i].max < key:
          i += 1
      self.children[i]._insert_non_full(key)

  def _split_child(self, child, i):
    """
    Split the full child of a node

    Only leaf nodes have keys, and only non-leafs
    have children

    Here is where min and max pointers are modified

    Here is also where level-set pointers are assigned

    """
    node = self._create_new()
    node.parent = self
    node.left = child
    child.right = node

    if child.is_leaf():
      for _ in range(self.t):
        node.keys.append(child.keys.pop())
      node.keys.reverse()
      node.min = node.keys[0]
      node.max = node.keys[-1]
      child.max = child.keys[-1]
    else:
      for _ in range(self.t):
        node.children.append(child.children.pop())
      node.children.reverse()
      node.min = node.children[0].min
      node.max = node.children[-1].max
      child.max = child.children[-1].max
    self.children = \
      self.children[:i + 1] + [node] + self.children[i + 1:]


  def insert(self, key):
    """
    Insert values into a tree where data is only stored
    in the leaves

    Each node also has min and max pointers, as well as
    level-set pointers

    """
    # Update min and max
    if self.min is None or key < self.min:
      self.min = key
    if self.max is None or key > self.max:
      self.max = key
    # Update the node
    if self.n == 0: # empty root case
      self.keys.append(key)
      return self
    if self.n == self.max_capacity: # root is full case
      node = self._create_new()
      node.children.append(self)
      self.parent = node
      node.min = self.min
      node.max = self.max
      node._split_child(self, 0)
      node.children[node.children[0].max < key]._insert_non_full(key)
      return node
    self._insert_non_full(key)
    return self
