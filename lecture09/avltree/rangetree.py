"""
1-D Range Tree
--------------

Range trees are data structures optimized
to query for all nodes and subtrees with
keys in a provided interkey in logarithmic
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
  def __init__(self, key):
    AVLTreeNode.__init__(self, key)

  def search(self, key):
    """
    Search function is modified for range queries
    so that if a keyue is not in the tree, it'll
    return the leaf node whose subtree would contain
    the keyue being queried

    """
    if self.key == key and self.left is None:
      return self
    if self.key == key:
      return self.left.search(key)
    if key < self.key and self.left is None:
      return self
    if key < self.key:
      return self.left.search(key)
    if key > self.key and self.right is None:
      return self
    return self.right.search(key)


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
    of keyues L

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

