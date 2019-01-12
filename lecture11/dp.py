"""
Lecture 11: All-Pairs Shortest Paths
------------------------------------
Dynamic programming method

"""


from graph import Graph


def dp_all_pairs_shortest_paths(graph):
  """
  Get the shortest paths between all pairs of vertices
  using a bottom-up DP approach.

  The idea is you relax every edge V - 1 times and
  if each path is not the best possible one then there
  is a negative weight cycle.

  Complexity: O(v ** 4) where v is the number of vertices in the graph

  This algorithm is the slowest method considered in this lecture

  """
  if not isinstance(graph, Graph):
    raise TypeError(
      'dp_all_pairs_shortest_paths must be called with a Graph instance')
  dp = dict()
  parents = dict()
  for u in graph.vertices:
    for v in graph.vertices:
      dp[(u, v)] = graph.get_edge_weight(u, v)
      parents[(u, v)] = None
  for _ in range(graph.v - 1):
    for u in graph.vertices:
      for v in graph.vertices:
        for x in graph.vertices:
          if dp[(u, v)] > dp[(u, x)] + dp[(x, v)]:
            dp[(u, v)] = dp[(u, x)] + dp[(x, v)]
            parents[(u, v)] = x
  for u in graph.vertices:
    for v in graph.vertices:
      for x in graph.vertices:
        if dp[(u, v)] > dp[(u, x)] + dp[(x, v)]:
          raise Exception('Negative weight cycle')
  return (dp, parents)
