"""
Kruskal's Minimum Spanning Tree
Algorithm
---------

Kruskal's algorithm creates a minimum spanning tree (MST)
by sorting the edges by weight in descending order in a list,
and initializing a disjoint-set data structure containing all
vertices in singletons.

While the list is not empty, pop the last element in
the list, the edge with the least weight left.

If the vertices in the edge are not in the same set in the
disjoint-set, concatenate their sets and add that edge to
the MST.

"""


from disjointset import DisjointSet
from graph import Graph


def kruskals_algorithm_mst(graph):
  """
  Kruskal's algorithm to find the minimum
  spanning tree of a connected, undirected,
  weighted graph.

  This implementation runs in

  O(sort(e) + (e * a(v)) + v)

  where a is inverse Ackermann function
  (https://en.wikipedia.org/wiki/Ackermann_function)
  and is generally considered a constant

  The sort in this case is O(e * log(e)) but
  if you can use counting sort or radix sort it can
  be reduced to O(e)

  This algorithm makes its greedy choice starting with
  the globally minimum weighted edge, and then continues
  selecting edges until it forms a spanning tree.

  """
  if not isinstance(graph, Graph):
    raise TypeError(
      'kruskals_algorithm_mst expects a Graph as an argument')
  ds = DisjointSet()
  T = set()
  for u in graph.vertices:
    ds.make_set(u)
  edges = []
  visited = set()
  for u, v in graph.weights:
    if (v, u) not in visited:
      visited.add((u, v))
      edges.append((u, v))
  edges.sort(
    key=lambda k: graph.weights[k], reverse=True)
  while edges:
    u, v = edges.pop()
    if ds.find_set(u) != ds.find_set(v):
      ds.union(u, v)
      T.add((u, v))
  return T
