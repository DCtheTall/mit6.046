"""
Prim's Algorithm
----------------

This is an implementation of Prim's algorithm
for finding the minimum spanning tree (MST) of
a connected, undirected, weighted graph.

"""


from graph import Graph
from priorityqueue import PriorityQueue


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


def prims_algorithm_mst(graph):
  """
  Prim's algorithm, this algorithm
  has the same time complexity as Djikstra's
  single source shorted path algorithm.

  This particular algorithm is

  O((V ** 2) + (V * E))

  but with a priority queue or vEB tree this can be reduced
  to

  O((V * log(V)) + (V * E))

  a time complexity equivalent to Djikstra's

  """
  if not isinstance(graph, Graph):
    raise TypeError(
      'this function expects an instance of Graph')
  queue = PriorityQueue(graph)
  root = None
  nodes = {
    u: TreeNode(u)
    for u in graph.vertices
  }
  while not queue.is_empty():
    u = queue.pop_min()
    if root is None:
      root = nodes[u]
    for v in graph.adj[u]:
      if queue.contains(v):
        queue.update(v, graph.weights[(u, v)])
        nodes[v].parent = nodes[u]
  for n in nodes:
    node = nodes[n]
    if node.parent is not None:
      node.parent.children.append(node)
  return root
