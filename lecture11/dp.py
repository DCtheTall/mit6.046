"""
All-Pairs Shortest Paths
------------------------
First dynamic programming method

"""


class Graph(object):
  """
  Graph data structure which uses an adjacency
  matrix to keep track of edge weights

  """
  def __init__(self, vertices):
    self.vertices = vertices
    self.v = len(vertices)
    self.edges = [
      [
        0 if u == v else float('inf')
        for v in vertices
      ]
      for u in vertices
    ]

  def get_edge_weight(self, u, v):
    """
    Get weight of edge from vertex u to vertex v

    """
    if u not in self.vertices or \
      v not in self.vertices:
        raise KeyError('Vertices not in the graph')
    return self.edges[u][v]

  def set_edge_weight(self, u, v, weight):
    """
    Set the weight of an edge in the graph

    """
    if u not in self.vertices or \
      v not in self.vertices:
        raise KeyError('Vertices not in the graph')
    self.edges[u][v] = weight


def dp_all_pairs_shortest_paths(graph):
  """
  Get the shortest paths between all pairs of vertices
  using a bottom-up DP approach.

  The idea is you relax every edge V - 1 times

  Complexity: O(v ** 4) where v is the number of vertices in the graph

  """
  dp = dict()
  parents = dict()
  for u in graph.vertices:
    parents[u] = None
    for v in graph.vertices:
      dp[(u, v)] = graph.get_edge_weight(u, v)
  for _ in range(graph.v - 1):
    for u in graph.vertices:
      for v in graph.vertices:
        for x in graph.vertices:
          if dp[(u, v)] > dp[(u, x)] + dp[(x, v)]:
            dp[(u, v)] = dp[(u, x)] + dp[(x, v)]
