"""
Lecture 11: All-Pairs Shortest Paths
Johnson's Algorithm
-------------------
Johnson's algorithm in summary is creating a way
to run Djikstra's algorithm on any arbitrary graph
that does not have negative weight cycles.

It does so by finding a function

h: V -> R

where forall u, v in V

w(u, v) + h(u) - h(v) >= 0

This is achieved by running Bellman-Ford once
on a non-existent source vertex s which we treat
as being connected to every v in V with w(s, v) = 0

The resulting function h(u) = d(s, u) where d(s, u) is the
shortest path from s to u.

The condition for h is met because

w(u, v) + d(s, u) - d(s, v) >= 0

is equivalent to

d(s, v) <= d(s, u) + w(u, v)

which is true if d(s, v) is the shortest path from
the source vertex to v

"""


from graph import Graph


def bellman_ford(graph):
  """
  Bellman-Ford single-source
  shortest path algorithm

  The algorithm is augmented for Floyd-Warshall,
  which adds a source vertex connected to every
  other vertex with a weight of 0

  Given a graph (V, E, w)

  The point of this is to define a function

  h: V -> R

  where forall u, v in V

  w(u, v) + h(u) - h(v) >= 0

  This function allows us to use Djikstra's shortest
  path algorithm from each vertex

  Bellman-Ford also handles detecting any
  negative weight cycles

  """
  result = {u: 0 for u in graph.vertices}
  for _ in range(graph.v - 1):
    for u in graph.vertices:
      for v in graph.vertices:
        if result[u] > result[v] + graph.get_edge_weight(v, u):
          result[u] = result[v] + graph.get_edge_weight(v, u)
  for u in graph.vertices:
    for v in graph.vertices:
      if result[u] > result[v] + graph.get_edge_weight(v, u):
        raise Exception('Negative weight cycle')
  return result


def djikstra(graph, h, src, costs, parents):
  """
  Djikstra's algorithm finding the shortest path in a
  graph (V, E, w) where

  w(u, v) + h[u] - h[v] >= 0

  It finds the shortest paths to each vertex from
  a given source vertex src and records it in the
  result of the Floyd-Warshall implementation
  below

  This particular implementation is O((v ** 2) + (v * e))

  but O((v * log(v)) + (v * e)) is possible using an augmented heap

  """
  unfinished = {
    u: float('inf')
    for u in graph.vertices
  }
  unfinished[src] = 0
  visited = set()
  while unfinished:
    u = min(unfinished, key=unfinished.get)
    costs[(src, u)] = unfinished[u]
    visited.add(u)
    del unfinished[u]
    for v in graph.vertices:
      if v in visited:
        continue
      if (unfinished[v] + h[src] - h[v]) > \
        (costs[(src, u)] + graph.get_edge_weight(u, v) + h[src] - h[v]):
          unfinished[v] = \
            costs[(src, u)] + graph.get_edge_weight(u, v)
          parents[(src, v)] = u


def johnsons_algorithm(graph):
  """
  Floyd-Warshall algorithm for finding the shortest paths
  between all pairs of points in a graph (V, E, w).

  It uses Bellman-Ford's algorithm to find a function

  h: V -> R

  where forall u, v in V:

  w(u, v) + h[u] - h[v] >= 0

  Which allows us to run Djikstra's algorithm on each vertex

  Complexity: O(((v ** 2) * log(v)) + (v * e))

  which for dense graphs is just O(v ** 3)

  on a dense graph which is the best performance known
  without special matrix multiplication algorithms on
  different formulations of the matrix multiplication
  method

  """
  if not isinstance(graph, Graph):
    raise TypeError(
      'bellman_ford must be called with an instance of Graph')
  h = bellman_ford(graph)
  costs = dict()
  parents = dict()
  for u in graph.vertices:
    for v in graph.vertices:
      costs[(u, v)] = 0 if u == v else float('inf')
      parents[(u, v)] = None
  for src in graph.vertices:
    djikstra(graph, h, src, costs, parents)
  return (costs, parents)
