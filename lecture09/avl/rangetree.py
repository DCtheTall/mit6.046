"""
Lecture 9: Augmentation
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
from collections import deque


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
    the key being queried

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
      node.min = L[0]
      node.max = L[1]
      node.left = RangeTreeNode(L[0])
      node.left.min = node.left.max = L[0]
      node.right = RangeTreeNode(L[1])
      node.right.min = node.right.max = L[1]
      node.left.parent = node.right.parent = node
      return node

    mid = n // 2
    if n == 1:
      return
    node = RangeTreeNode(L[mid])
    node.min = L[0]
    node.max = L[-1]

    L_left = L[:mid + 1]
    node.left = RangeTree.build(L_left)
    node.left.parent = node
    node.left.min = L_left[0]
    node.left.max = L_left[-1]

    L_right = L[mid + 1:]
    node.right = RangeTree.build(L_right)
    node.right.parent = node
    node.right.min = L_right[0]
    node.right.max = L_right[-1]

    return node

  def _lowest_common_ancestor(self, left, right):
    """
    Find the lowest common ancestor
    of the two leaf nodes at the edge of the
    range

    """
    tmp = left
    while tmp.max < right.key and \
      tmp.parent is not None:
        tmp = tmp.parent
    return tmp

  def range_search(self, lo, hi):
    """
    Return all nodes in the given range.
    The function returns a list of all nodes
    and all subtrees in the given range.

    """
    left = self.root.search(lo)
    right = self.root.search(hi)
    lca = self._lowest_common_ancestor(left, right)
    nodes = deque()
    trees = deque()
    if left.key > lo:
      nodes.append(left)
    cur = left
    while cur != lca:
      if cur.key > lo and cur.right is not None:
        nodes.appendleft(cur)
        trees.appendleft(cur.right)
      cur = cur.parent
    if right.key < hi:
      nodes.append(right)
    cur = right
    while cur != lca:
      if cur.key < hi and cur.left is not None:
        nodes.append(cur)
        trees.append(cur.left)
      cur = cur.parent
    return (list(nodes), list(trees))
