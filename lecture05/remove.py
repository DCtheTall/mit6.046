"""
B-Tree: Deletion
----------------
A B-tree node with only deletion implemented

"""


from insert import BTreeInsertNode


class BTreeDeleteNode(BTreeInsertNode):
  """
  Inherits from BTreeInsertNode in insert.py
  which inherits from BTreeSearchNode in search.py

  """
  def __init__(self, t):
    BTreeInsertNode.__init__(self, t)

  def _create_new(self):
    """
    Overwrite _create_new for the insertion
    methods

    """
    return BTreeDeleteNode(self.t)

  def _find_key(self, key):
    """
    Find which index a key is stored in a node
    or which index the child where the key may be

    """
    i = 0
    while i < self.n and self.keys[i] < key:
      i += 1
    return i

  def _get_predecessor(self, i):
    """
    Gets the immediate predecessor of the key
    at index i of this node

    """
    cur = self.children[i]
    while not cur.is_leaf():
      cur = cur.children[cur.n]
    return cur.keys[cur.n - 1]

  def _get_successor(self, i):
    """
    Gets the immediate successor of the key
    at index i of this node

    """
    cur = self.children[i + 1]
    while not cur.is_leaf():
      cur = cur.children[0]
    return cur.keys[0]

  def _borrow_from_prev(self, i):
    """
    This function adds a key to child i
    by borrowing the last key from its left sibling
    which replaces a key in the current node (self)
    the replaced key is passed down to the child as
    a new key

    If the child is not a leaf, this also borrows the rightmost child
    node of the sibling and adds it as the leftmost child node

    """
    child = self.children[i]
    sibling = self.children[i - 1]

    child.keys = [self.keys[i - 1]] + child.keys
    self.keys[i - 1] = sibling.keys.pop()

    if not child.is_leaf():
      child.children = [sibling.children.pop()] + child.children

  def _borrow_from_next(self, i):
    """
    Similar to _borrow_from_prev but mirrored in the other direction

    Adds a key to child i by borrowing a key from its right sibling
    which replaces a key in this node (self) and passes it to child

    If child is not a leaf, it also appends the siblings leftmost child

    """
    child = self.children[i]
    sibling = self.children[i + 1]

    child.keys = child.keys + [self.keys[i]]
    self.keys[i] = sibling.keys.pop(0)

    if not child.is_leaf():
      child.children = \
        child.children.append(sibling.children.pop(0))

  def _merge(self, i):
    """
    Merge two children at indexes i and i + 1
    which each have t - 1 keys into a single
    child which will have (2 * t) - 1 keys. It does
    so by borrowing a key i from the current node (self)
    and then truncating the key and children keys in self
    to remove the gap created by merging two children

    """
    child = self.children[i]
    sibling = self.children[i + 1]
    child.keys.append(self.keys.pop(i))
    child.keys += sibling.keys
    if not child.is_leaf():
      child.children += sibling.children
    self.children.pop(i + 1)

  def _fill(self, i):
    """
    Fill a child which has only t - 1 keys so that
    a delete operation or a merge on two of its children
    can be done with this current node

    """
    if i != 0 and self.children[i - 1].n >= self.t:
      self._borrow_from_prev(i)
    elif i != self.n and self.children[i + 1].n >= self.t:
      self._borrow_from_next(i)
    else:
      self._merge(i - 1 if i == self.n else i)

  def _remove_from_leaf(self, i):
    """
    Remove the key at index i from this node,
    given that it is a leaf

    """
    self.keys.pop(i)
    return self

  def _remove_from_non_leaf(self, i):
    """
    Remove the key at index i from a non-leaf node

    """
    key = self.keys[i]
    if self.children[i].n >= self.t:
      # If the child has >= t keys, get the immediate predecessor
      # of key and replace key in self.keys, then delete the predecessor
      # from the child node recursively
      pred = self._get_predecessor(i)
      self.keys[i] = pred
      self.children[i] = self.children[i].remove(pred)
      return self
    if self.children[i + 1].n >= self.t:
      # If the child to the right of the node has >= t keys, get the
      # immediate successor of key and replace key in self.keys, then
      # delete the successor from the child node recursively
      succ = self._get_successor(i)
      self.keys[i] = succ
      self.children[i + 1] = self.children[i + 1].remove(succ)
      return self
    # If both children do not have enough keys, merge key and both children into
    # child i, afterwards child i will have (2 * t) - 1 keys. Then recursively
    # delete the key from the newly merged child
    self._merge(i)
    self.children[i] = self.children[i].remove(key)
    return self

  def remove(self, key):
    """
    Remove key from the B-tree rooted at this node

    """
    i = self._find_key(key)
    if i < self.n and self.keys[i] == key:
      if self.is_leaf():
        return self._remove_from_leaf(i)
      return self._remove_from_non_leaf(i)
    if self.is_leaf():
      raise KeyError(
        'key {} is not in B-tree'.format(key))
    key_in_last_child = i == self.n
    if self.children[i].n < self.t:
      # if deleting from the child will result in it having to few nodes,
      # we borrow a key from its other children
      self._fill(i)
    if key_in_last_child and i > self.n:
      i -= 1
    self.children[i] = self.children[i].remove(key)
    if len(self.children) == 1:  # case when root has only one child
      return self.children[0]
    return self
