"""
Order Statistic Tree
--------------------
An augmented AVL tree which can
compute the rank of each node and
select a node at particular rank in
O(log(N)) time

"""


from avl import TreeNode


class OrderStatisticNode(TreeNode):
  """
  OrderStatisticNode has some extended properties
  of the TreeNode in avl.py

  """
  def __init__(self, val):
    TreeNode.__init__(self, val)

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

