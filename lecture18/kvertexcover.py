"""
Lecture 18: Fixed Parameter Algorithms
k-Vertex Cover
--------------
Given an undireced graph G(V, E) and an integer k,
we want to find if there exists a subset of V, S,
such that |S| <= k and for all (u, v) in E, either
u is in S or v is in S (or both).

This is known as the k-Vertex Cover problem, it is
a modified version of the NP-hard Vertex Cover problem
covered in lecture 17.

The kVC problem is an example of a fixed-parameter
tractable (FPT) problem. An FPT problem is an NP-hard
problem whose exponential runtime depends on a fixed
parameter, in this case, the integer k.

"""


from itertools import combinations


class Graph(object):
  """
  Implementation of an undirected graph
  where each vertex has a degree >= 1

  This class is used for the different
  k-Vertex Cover algorithms covered in
  this lecture.

  """
  def __init__(self, edges):
    self.edges = edges
    self.vertices = set()
    self.adj = dict()
    for u, v in edges:
      self.vertices.add(u)
      self.vertices.add(v)
      try:
        self.adj[u].add(v)
      except:
        self.adj[u] = {v}
      try:
        self.adj[v].add(u)
      except:
        self.adj[v] = {u}


def brute_force_k_vertex_cover(graph, k):
  """
  The brute force method for the k-Vertex Cover
  problem is to choose every possible combination
  of k vertices in the graph and see if any
  of them form a vertex cover.

  This time complexity of this algorithm is

  O(EV^k)

  since the number of combinations of k vertices
  grows exponentially with respect to V.

  """
  if not isinstance(graph, Graph):
    raise TypeError(
      'the first argument of brute_force_k_vertex_cover must be an instance of Graph')
  if len(graph.vertices) < k:
    raise Exception(
      'k must not be greater than the number of vertices in the graph')
  for S in combinations(graph.vertices, k):
    for u, v in graph.edges:
      if u not in S and v not in S:
        break
    else:
      return True
  return False
