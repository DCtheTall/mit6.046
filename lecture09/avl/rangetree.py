"""
1-D Range Tree
--------------

Range trees are data structures optimized
to query for all nodes and subtrees with
keys in a provided interval in logarithmic
time

This is an example of a 1-D range tree
which stores integers

Implementation is based on the code here:
http://www.cs.uu.nl/docs/vakken/ga/slides5b.pdf

"""


from avl import AVLTreeNode


class RangeTreeNode(AVLTreeNode):
  """
  RangeTreeNode inherits properties from the AVLTreeNode
  but has a modified search method

  """
  def __init__(self, val):
    AVLTreeNode.__init__(self, val)

  def search(self, val):
    """
    Search function is modified for range queries
    so that if a value is not in the tree, it'll
    return the leaf node whose subtree would contain
    the value being queried

    """
    if self.val == val and self.left is None:
      return self
    if self.val == val:
      return self.left.search(val)
    if val < self.val and self.left is None:
      return self
    if val < self.val:
      return self.left.search(val)
    if val > self.val and self.right is None:
      return self
    return self.right.search(val)


class RangeTree(object):
  """
  1-D Range tree class built using a list
  of integers

  """
  def __init__(self, L):
    self.root = RangeTree.build(L)

  @staticmethod
  def build(L):
    """
    Construct a range tree structure from a list
    of values L

    """
    n = len(L)
    if n == 0:
      return None
    if n == 1:
      return RangeTreeNode(L[0])
    if n == 2:
      node = RangeTreeNode(L[0])
      node.left = RangeTreeNode(L[0])
      node.right = RangeTreeNode(L[1])
      node.left.parent = node.right.parent = node
      return node
    mid = n // 2
    node = RangeTreeNode(L[mid])
    node.left = RangeTree.build(L[:mid + 1])
    if node.left is not None:
      node.left.parent = node
    node.right = RangeTree.build(L[mid + 1:])
    if node.right is not None:
      node.right.parent = node
    return node

  def range_query(self, lo, hi):
    left = self.root.search(lo)
    right = self.root.search(hi)
    # TODO find LCA of left and right


t = RangeTree(range(0, 100, 2))

