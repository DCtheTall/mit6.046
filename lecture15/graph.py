"""
Lecture 15: Linear Programming
Directed Graph w Non-negative Edge Weights
------------------------------------------

This program contains a class definition for a
directed graph with edge weights that are >= 0.

The graph will be used for a single source shortest
path algorithm, but this time we will use linear
programming instead of Djikstra's to find the shortest
path from the source to each vertex. The example graph
that will be used is from this Djikstra's example:

https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/

which has the shortest paths from the source vertex, 0,
all given.

"""


class Graph(object):
  """
  Graph class to be used in linprog.py
  as an example of using linear programming
  to find the shortest path to each vertex
  from a given source vertex.

  """
  def __init__(self, edge_weights):
    self.vertices = set()
    self.adjacency_list = dict()
    for u, v in edge_weights:
      if edge_weights[(u, v)] < 0:
        raise Exception(
          'Cannot have negative edge weights')
      self.vertices.add(u)
      self.vertices.add(v)
      try:
        self.adjacency_list[u].add(v)
      except:
        self.adjacency_list[u] = {v}
    for u in self.vertices:
      if u not in self.adjacency_list:
        self.adjacency_list[u] = set()
    self.edge_weights = edge_weights
