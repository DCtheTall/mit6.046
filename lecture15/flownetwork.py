"""
Lecture 15: Linear Programming
Flow Network
------------

Below is a class that will be used as a data structure representing
a residual flow network which will be used for finding the maximum
flow allowable through a flow network. See lecture 13-14 for more
information.

This data structure is used in linprog.py for finding the
max flow using linear programming.

"""


class FlowNetwork(object):
  """
  ResidualNetwork class represents the
  residual network of a given a flow network
  using a graph with adjacency lists keeping
  track of residual capacity going through each
  edge and the flow through each edge

  """

  def __init__(self, src, sink, capacities):
    self.src = src
    self.sink = sink
    self.residual_capacities = capacities
    self.adj = dict()
    self.flows = dict()
    self.vertices = set()
    for u, v in capacities:
      try:
        self.adj[u].add(v)
      except:
        self.adj[u] = {v}
      try:
        self.adj[v].add(u)
      except:
        self.adj[v] = {u}
      self.flows[(u, v)] = 0
      self.vertices.add(u)
      self.vertices.add(v)

  def residual_network_bfs(self):
    """
    Perform a BFS on the residual netowrk
    and return a tuple containing if a path
    from the source to the sink exists and
    the parent pointers for that path

    Complexity: O(V + E_f) (BFS)

    where V is the set of vertices in the flow/residual network
    and E_f is the set of edges in the residual network

    """
    frontier = [self.src]  # queue
    parents = {self.src: None}
    while frontier:
      new_frontier = []
      for u in frontier:
        if u == self.sink:
          return (True, parents)
        for v in self.adj:
          if v in parents:
            continue
          if (u, v) in self.residual_capacities and \
                  self.residual_capacities[(u, v)] > 0:
              parents[v] = u
              new_frontier.append(v)
          # recall residual capacity networks have flow edges
          # always >= 0 and the edge direction is against the
          # actual direction of the flow
          elif (v, u) in self.flows and \
                  self.flows[(v, u)] > 0:
              parents[v] = u
              new_frontier.append(v)
      frontier = new_frontier
    return (False, parents)
