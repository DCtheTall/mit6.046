"""
B-Tree: Searching
-----------------
A B-tree class which only implements searching

"""


class BTreeSearchNode(object):
  """
  B-tree node initialized with a list to keep track of keys,
  some comparable type, let's say ints and a list for children
  which will contain other B-tree nodes

  Let the minimum degree denote the minimum number of children
  any node must have, given said node is not the root

  """

  def __init__(self, t):  # minimum degree t
    self.t = t
    self.max_capacity = (2 * t) - 1
    self.keys = []
    self.children = []

  @property
  def n(self):
    """
    'n' property stores the number of keys
    Easiest way to keep a running count of the number
    of keys without having to repeat code

    """
    return len(self.keys)

  def is_leaf(self):
    """
    Returns true if the node is a leaf node

    """
    return len(self.children) == 0

  def search(self, key):
    """
    Returns the node where the key is in,
    if the key is not in the tree it
    returns None

    Assumes B-tree is non-empty

    """
    i = 0
    while i < self.n and self.keys[i] < key:
      i += 1
    if i < self.n and self.keys[i] == key:
      return self
    if self.is_leaf():
      return None
    return self.children[i].search(key)

  def traverse(self, root=True):
    """
    Print the tree inorder

    """
    # first test that the tree is balanced
    if not root and \
      (self.n < (self.t - 1) or \
        self.n > ((2 * self.t) - 1)):
          raise Exception
    result = ' - '
    for i in range(self.n):
      if not self.is_leaf():
        result += self.children[i].traverse(False)
      result += '{} '.format(self.keys[i])
    if not self.is_leaf():
      result += self.children[-1].traverse(False)
    return result
