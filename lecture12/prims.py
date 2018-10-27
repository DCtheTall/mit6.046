"""
Prim's Algorithm
----------------

This is an implementation of Prim's algorithm
for finding the minimum spanning tree (MST) of
a connected, undirected, weighted graph.

"""


from graph import Graph
from treenode import TreeNode
from random import sample


class PriorityQueue(object):
  """
  PriorityQueue which has the ability to update the
  value of a key, and pop the key with the minimum
  value.

  The efficiency of this can be improved if you
  use a vEB tree as the underlying data structure
  for large graphs.

  """

  def __init__(self, graph):
    src = sample(graph.vertices, 1)
    self.data = {
      u: 0 if u == src else float('inf')
      for u in graph.vertices
    }

  def is_empty(self):
    """
    Returns if queue is empty

    """
    return len(self.data) == 0

  def contains(self, key):
    """
    Returns a bool representing if key is in the queue

    """
    return key in self.data

  def update(self, key, val):
    """
    Update the priority (val) of a key in the queue

    """
    self.data[key] = val

  def pop_min(self):
    """
    Pop key with minimum priority in O(n) time

    """
    u = min(self.data, key=self.data.get)
    del self.data[u]
    return u



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
