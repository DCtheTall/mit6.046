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

"""


from remove import BTreeDeleteNode as BTreeNode


class FingerSearchBTree(object):
  """
  B-tree class using the augmented nodes
  that satisfy the finger-search property

  """

  def __init__(self, T, t):
    self.type = T
    self.root = None
    self.t = t

  def _type_check(self, key):
    """
    Type check if the a key is the right type
    for the tree

    """
    if not isinstance(key, self.type):
      raise TypeError(
        '{} is not the correct type'.format(key))

  def search(self, key):
    """
    Search the B-tree for the node
    containing a provided key

    """
    self._type_check(key)
    if self.root is None:
      return None
    return self.root.search(key)

  def insert(self, key):
    """
    Insert a provided key into the tree

    """
    self._type_check(key)
    if self.root is None:
      self.root = BTreeNode(self.t)
    self.root = self.root.insert(key)

  def remove(self, key):
    """
    Remove a key from the tree

    """
    self._type_check(key)
    if self.root is None:
      raise KeyError(
          'key {} is not in B-tree'.format(key))
    self.root = self.root.remove(key)

  def traverse(self):
    """
    Traverse the tree and return the values inorder

    """
    if self.root is None:
      return ''
    return self.root.traverse()

  def finger_search(self, src, dst):
    """
    Search for a node, dst, from a key or from a provided node

    This tree obeys the finger-search property, meaning
    that this takes no more than O(log(abs(rank(src) - rank(dst))))

    """
    if isinstance(src, self.type):
      src = self.search(src)
      if src is None:
        raise KeyError(
          '{} is not in B-tree'.format(src))
    if not isinstance(src, BTreeNode):
      raise TypeError(
        'Unexcepted 1st argument to finger_search')
    if src.min <= dst and dst <= src.max:
      return src.search(dst)
    if dst < src.min:
      src = src.left
    elif dst > src.max:
      src = src.right
    src = src.parent
    if src is None:
      return None
    return self.finger_search(src, dst)
