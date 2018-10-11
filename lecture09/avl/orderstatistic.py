"""
Order Statistic Tree
--------------------
An augmented AVL tree which can
compute the rank of each node and
select a node at particular rank in
O(log(N)) time

"""


from avl import AVLTreeNode, BinaryTree


class OrderStatTreeNode(AVLTreeNode):
  """
  OrderStatisticNode has some extended properties
  of the TreeNode in avl.py

  """
  def __init__(self, val):
    AVLTreeNode.__init__(self, val)

  def _create_new(self, val):
    return OrderStatTreeNode(val)

  def rank(self):
    """
    Get the rank of the node (i.e. the index of the node in an ordered list)

    """
    r = 0 if self.left is None else self.left.size
    tmp = self
    while tmp.parent is not None:
      tmp = tmp.parent
      if tmp.val < self.val:
        r += 0 if tmp.left is None else tmp.left.size
    return r

  def select(self, i):
    """
    Get the node with rank i from the root

    """
    r = 0 if self.left is None else self.left.size
    if i == r:
      return self
    if i < r:
      return self.left.select(i)
    return self.right.select(i - r)


class OrderStatisticTree(BinaryTree):
  """
  Order-statistic tree can do normal
  binary search tree operations in O(log(N)) time

  Can also find the rank of a provided value in the
  tree
  """
  def __init__(self):
    BinaryTree.__init__(self, OrderStatTreeNode)

  def rank(self, val):
    """
    Select the rank of a value in the OrderStatisticTree

    """
    if self.root is None:
      raise Exception(
        '{} is not in OrderStatisticTree, tree is empty'.format(val))
    node = self.search(val)
    if node is None:
      return -1
    return node.rank(val)

  def select(self, i):
    """
    Select the node at rank i in the tree

    """
    if self.root is None or i > self.root.size:
      raise IndexError(
        'Rank {} out of range'.format(i))
    return self.root.select(i)
