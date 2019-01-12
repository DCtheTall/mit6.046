"""
Lecture 11: All-Pairs Shortest Paths
Floyd-Warshall All-Pairs
Shortest Path Algorithm
-----------------------

This is a method to find the shortest paths between
all pairs of vertices in a graph (V, E, w)
using dynamic programming.

The recursion to get the shortest paths d[(u, v)]
is given by:

for k in V:
  for u, v in E:
    d[(u, v)] =
      min([
        d[(u, v)],
        d[(u, k)] + d[(k, v)],
      ])

"""


from graph import Graph


def floyd_warshall(graph):
  """
  Floyd-Warshall Python implementation

  This is a recursive method for doing the
  same computation as the matrix multiplication
  but in a more efficient way.

  Complexity: O(v ** 3)

  """
  if not isinstance(graph, Graph):
    raise TypeError(
      'floyd_warshall expected a Graph instance')
  costs = dict(graph.edges)
  parents = {
    (u, v): u
    for u, v in costs
  }
  for k in graph.vertices:
    for u in graph.vertices:
      for v in graph.vertices:
        if costs[(u, v)] > (costs[(u, k)] + costs[(k, v)]):
          costs[(u, v)] = costs[(u, k)] + costs[(k, v)]
          parents[(u, v)] = k
  for k in graph.vertices:
    for u in graph.vertices:
      for k in graph.vertices:
        if costs[(u, v)] > (costs[(u, k)] + costs[(k, v)]):
          raise Exception('Negative weight cycle')
  return (costs, parents)

