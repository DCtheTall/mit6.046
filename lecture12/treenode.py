"""
TreeNode class is a general type
for the minimum spanning trees I will
be computing using Prim's and Kruskal's
algorithm

"""


class TreeNode(object):
  """
  TreeNode class

  property: {any hashable type} key
  property: {TreeNode} parent
  property: {list(TreeNode)} children
  """
  def __init__(self, key):
    self.key = key
    self.parent = None
    self.children = []
