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
    self.adj = dict()
    self.weights = dict()
    for u, v in edge_weights:
      # No directed edges, each pair of vertices can only appear once
      if (v, u) in edge_weights:
        raise TypeError(
          'Graph can include each pair of vertices once')
      self.weights[(u, v)] = self.weights[(v, u)] = edge_weights[(u, v)]
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
      # BFS to check connectedness
      visited = set()
      frontier = [u]
      while frontier:
        new_frontier = []
        for u in frontier:
          if u in visited:
            continue
          visited.add(u)
          for v in self.adj[u]:
            new_frontier.append(v)
        frontier = new_frontier
      if visited.difference(self.vertices):
        raise TypeError('Graph must be connected')
