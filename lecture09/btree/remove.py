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

This program covers methods for each node used for removing keys

"""


from insert import BTreeInsertNode


class BTreeDeleteNode(BTreeInsertNode):
  """
  Augmented B-tree node where only the leaf
  nodes have keys and non-leaf nodes have children

  Each node has a pointer to its min, max elements
  and its left and right siblings

  """
  def __init__(self, t):
    BTreeInsertNode.__init__(self, t)

  def _create_new(self):
    """
    Create a new instance of the node

    """
    return BTreeDeleteNode(self.t)

  def _get_val_at_index(self, i):
    """
    Get the value at index i to compare to
    a key when finding the index in the
    method below

    """
    if self.is_leaf():
      return self.keys[i]
    return self.children[i].max

  def _find_key(self, key):
    """
    Find the index of a key in a node's keys if it
    is a leaf, or its children if it is not a leaf

    """
    i = 0
    while i < self.n and \
      self._get_val_at_index(i) < key:
        i += 1
    return i

  def _remove_from_leaf(self, key, i):
    """
    Remove a key from a leaf node, its parent's remove method
    ensures the tree follows the B-tree balancing rules

    """
    if i == self.n or self.keys[i] != key:
      raise KeyError(
        '{} not in B-tree'.format(key))
    self.keys.pop(i)
    return self

  def _fill(self, i):
    pass

  def _merge(self, i):
    pass

  def remove(self, key):
    """
    Remove key from the current node
    if the key is not in the tree it will
    raise a KeyError

    """
    if key < self.min or key > self.max:
      raise KeyError(
        '{} not in B-tree'.format(key))
    i = self._find_key(key)
    # If the tree is a leaf, then just pop the key at index i
    # If the key at i is not equal to self.keys[i] then its not
    # in the tree
    if self.is_leaf():
      self._remove_from_leaf(key, i)
    # The condition at the top guarantees that the key
    # should be in one of a non-leaf's children's range
    if self.children[i].n > self.t:
      self.children[i] = self.children[i].remove(key)
      return self
    # If possible, take a child or key from a siblight
    key_in_last_child = i == (self.n - 1)
    if self.children[i].n <= self.t:
      # if deleting from the child will result in it having to few nodes,
      # we borrow a key from its other children
      self._fill(i)
    if key_in_last_child and i == self.n:
      i -= 1
    self.children[i] = self.children[i].remove(key)
    if self.n == 1: # case when root has only one child
      return self.children[0]
    return self





