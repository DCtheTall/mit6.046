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
    self.max_capacity = 2 * t
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

  def is_leaf(self):
    """
    Returns true if the node is a leaf node

    """
    return len(self.children) == 0

  def traverse(self, root=True):
    """
    Print the tree inorder

    Also test that tree is balanced

    """
    if self.min is None or self.max is None:
      print self.children
      raise Exception('No range set')
    # first test that the tree is balanced
    if not root:
      if self.n < self.t or \
        self.n > self.max_capacity or \
        (not self.is_leaf() and len(self.keys)):
          raise Exception('imbalanced')
    result = ''
    if self.min > self.max:
      raise Exception('range incorrect')
    for i in range(self.n):
      if self.is_leaf():
        key = self.keys[i]
        if key < self.min or key > self.max:
          print self.keys, self.min, self.max
          raise Exception('key outside range')
        result += '{} '.format(self.keys[i])
      else:
        result += self.children[i].traverse(False)
    return result
