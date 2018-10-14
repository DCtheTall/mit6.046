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

  def _update_min(self):
    """
    Update the minimum values of each node on the left edge of the tree
    if the current subtrees minimum is being deleted

    """
    if self.is_leaf():
      self.min = self.keys[1]
    else:
      cur = self
      while not cur.is_leaf():
        cur = cur.children[0]
      self.min = cur.keys[1]

  def _update_max(self):
    """
    Update the maximum values of each node on the right edge of the tree
    if the current subtrees maximum is being deleted

    """
    if self.is_leaf():
      self.max = self.keys[-2]
    else:
      cur = self
      while not cur.is_leaf():
        cur = cur.children[-1]
      self.max = cur.keys[-2]

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

  def _borrow_from_prev(self, i):
    """
    This function borrows a key or child for one
    of the current node's children where the key
    we want to delete is

    In this case we borrow from the child's left sibling

    The augmented B-tree also has to modifiy the childrens'
    min and max pointers

    """
    child = self.children[i]
    sibling = child.left
    if child.is_leaf():
      child.keys = [sibling.keys.pop()] + child.keys
      child.min = child.keys[0]
      sibling.max = sibling.keys[-1]
    else:
      child.children = [sibling.children.pop()] + child.children
      child.min = child.children[0].min
      sibling.max = sibling.children[-1].max

  def _borrow_from_next(self, i):
    """
    This function borrows a key or child for one
    of the current node's children where the key
    we want to delete is

    In this case we borrow from the child's right sibling

    The augmented B-tree also has to modifiy the childrens'
    min and max pointers

    """
    child = self.children[i]
    sibling = child.right
    if child.is_leaf():
      child.keys = child.keys + [sibling.keys.pop(0)]
      child.max = child.keys[-1]
      sibling.min = sibling.keys[0]
    else:
      child.children = child.children + [sibling.children.pop(0)]
      child.max = child.children[-1].max
      sibling.min = sibling.children[0].min

  def _merge(self, i):
    """
    Merge a node's child i into i + 1

    This augmented B-tree also updates the max pointer
    and the level set pointer

    This occurs when each node only has t children or keys
    and deleting a child or key may result in violating the
    B-tree balancing rules

    This is the only place where a node can be deleted other
    than when the root only has 1 child after a merge

    """
    child = self.children[i]
    sibling = child.right
    child.right = sibling.right
    child.max = sibling.max
    if child.is_leaf():
      child.keys += sibling.keys
    else:
      child.children += sibling.children
    self.children.pop(i + 1)

  def _fill(self, i):
    """
    Fill a child which has only t keys or children so that
    a delete operation or a merge on two of its children
    can be done with this current node

    """
    if i != 0 and self.children[i - 1].n > self.t:
      self._borrow_from_prev(i)
    elif i != (self.n - 1) and self.children[i + 1].n > self.t:
      self._borrow_from_next(i)
    else:
      self._merge(i - 1 if i == (self.n - 1) else i)

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
    if key == self.min:
      self._update_min()
    elif key == self.max:
      self._update_max()
    # If the tree is a leaf, then just pop the key at index i
    # If the key at i is not equal to self.keys[i] then its not
    # in the tree
    if self.is_leaf():
      return self._remove_from_leaf(key, i)
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
      self.children[0].parent = None
      return self.children[0]
    return self
