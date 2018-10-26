"""
Minimum-Spanning Tree:

Graph
-----

This program contains a class definition for a
Graph for MST algorithms. Graphs for this algorithm
must have the following properties:

- The graph is connected
- The graph has weighted edges
- The edges are undirected

"""


class Graph(object):
  """
  Graph class takes a dictionary of edge weights of the format:

  {(u, v): w(u, v)}

  Each pair of points can only be included once. The constructor
  does a BFS to make sure the graph is connected

  """
  def __init__(self, edge_weights):
    if not edge_weights:
      raise TypeError(
        'Graph must include at least one edge')
    self.vertices = set()
    self.edges = dict()
    for u, v in edge_weights:
      # No directed edges, each pair of vertices can only appear once
      if u in self.edges and v in self.edges[u]:
        raise TypeError(
          'Graph can include each pair of vertices once')
      self.vertices.add(u)
      self.vertices.add(v)
      if u in self.edges:
        self.edges[u][v] = edge_weights[(u, v)]
      else:
        self.edges[u] = {v: edge_weights[(u, v)]}
      if v in self.edges:
        self.edges[v][u] = edge_weights[(u, v)]
      else:
        self.edges[v] = {u: edge_weights[(u, v)]}
      # BFS to check connectedness
      visited = set()
      frontier = [u]
      while frontier:
        new_frontier = []
        for u in frontier:
          if u in visited:
            continue
          visited.add(u)
          for v in self.edges[u]:
            new_frontier.append(v)
        frontier = new_frontier
      if visited != self.vertices:
        raise TypeError(
          'Graph must be connected')
