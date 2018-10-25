"""
Graph data structure to be used
for shortest path algorithms covered
in this lecture

"""


class Graph(object):
  """
  Graph data structure which uses an adjacency
  matrix to keep track of edge weights

  """

  def __init__(self, vertices):
    self.vertices = vertices
    self.v = len(vertices)
    self.edges = dict()
    for u in self.vertices:
        for v in self.vertices:
            self.edges[(u, v)] = 0 if u == v else float('inf')

  def get_edge_weight(self, u, v):
    """
    Get weight of edge from vertex u to vertex v

    """
    if u not in self.vertices or \
      v not in self.vertices:
        raise KeyError('Vertices not in the graph')
    return self.edges[(u, v)]

  def set_edge_weight(self, u, v, weight):
    """
    Set the weight of an edge in the graph

    """
    if u not in self.vertices or \
      v not in self.vertices:
        raise KeyError('Vertices not in the graph')
    self.edges[(u, v)] = weight
