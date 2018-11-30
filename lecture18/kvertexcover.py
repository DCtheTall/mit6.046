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
from random import sample


class Graph(object):
  """
  Implementation of an undirected graph
  where each vertex has a degree >= 1

  This class is used for the different
  k-Vertex Cover algorithms covered in
  this lecture.

  The constructor expects a set (or list)
  of 2-tuples representing each edge in
  the graph. Each element of the tuple
  is the key of the vertex on either end
  of the edge.

  """
  def __init__(self, edges):
    self.edges = edges
    self.vertices = set()
    for u, v in edges:
      self.vertices.add(u)
      self.vertices.add(v)

  def copy(self):
    """
    Return a copy of the graph instance
    with new objects

    """
    return Graph(set(self.edges))


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
  if not isinstance(k, int) or k <= 0 or len(graph.vertices) < k:
    raise Exception(
      'k must not be a positive integer greater than the number of vertices in the graph')
  for S in combinations(graph.vertices, k):
    for u, v in graph.edges:
      if u not in S and v not in S:
        break
    else:
      return True
  return False


def delete_vertex_and_edges(graph, u):
  """
  Returns a copy of the graph where u is deleted
  from the graphs vertices and all incident edges
  on u are deleted as well.

  """
  result = graph.copy()
  result.vertices.remove(u)
  for v, w in graph.edges:
    if u == v or u == w:
      result.edges.remove((v, w))
  return result


def bounded_search_tree_k_vertex_cover(graph, k):
  """
  Bounded search tree method for finding if a graph
  has a vertex cover S such that |S| <= k.

  The function starts by picking a random edge,
  (u, v) in E. Either u or v must be in any vertex
  cover of the graph. Then it makes 2 copies of the
  graph and deletes u from one copy and v from the,
  other and deletes any incident edges on the vertex
  that was deleted.

  The function then decrements k and calls itself recursively
  until k = 0. Once k is 0, then if a vertex cover exists, the
  graph should no longer have any edges remaining, otherwise
  no vertex cover, S, exists such that |S| <= k.

  """
  if not isinstance(graph, Graph):
    raise TypeError(
      'the first argument of brute_force_k_vertex_cover must be an instance of Graph')
  if not isinstance(k, int) or k < 0 or len(graph.vertices) < k:
    raise Exception(
      'k must not be a non-negative integer greater than the number of vertices in the graph')
  if k == 0:
    return len(graph.edges) == 0
  u, v = sample(graph.edges, 1)[0]
  graph_u = delete_vertex_and_edges(graph, u)
  graph_v = delete_vertex_and_edges(graph, v)
  return bounded_search_tree_k_vertex_cover(graph_u, k - 1) \
    or bounded_search_tree_k_vertex_cover(graph_v, k - 1)
