"""
Augmented B-Tree: Searching
---------------------------
This folder contains an implementation of an augmented B-tree.
For this implementation, the tree only stores data in its leaf
nodes. Each node also has level-set pointers defined here which
access the left and right siblings of each node (or None if they do not exist).
Each node also has a min/max key which store the minimum and maximum values
stored in the node or its children if it's not a leaf.

This implementation is optimized for finger-searching, i.e. finding a particular
value starting at a given node

This program covers methods for each node used for searching

"""


class BTreeSearchNode(object):
  """
  BTreeSearchNode

  A key difference between the implementation from lecture 5
  and this is that self.n refers to the number of children
  for non-leaf nodes

  """
  def __init__(self, t):
    self.t = t
    self.max_capacity = (2 * t) - 1
    self.keys = []
    self.children = []
    self.min = None
    self.max = None
    self.left = None
    self.right = None

  @property
  def n(self):
    """
    'n' property stores the number of keys if a leaf
    otherwise the number of children

    """
    if self.is_leaf():
      return len(self.keys)
    return len(self.children)

  @property
  def max_capacity(self):
    """
    Get the max capacity of the node

    """
    return (self.t << 1) - int(self.is_leaf())

  def is_leaf(self):
    """
    Returns true if the node is a leaf node

    """
    return len(self.children) == 0
