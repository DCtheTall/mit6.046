"""
Lecture 13: Max Flow Min Cut
----------------------------
This lecture covers flow networks and finding the maximum "flow"
that is possible to send through a flow network. A flow network
is a directed graph G(V, E) which has the following two
functions defined:

c: V x V -> R
f: V x V -> R

c(u, v) is called the capacity of the edge, it is the upper bound of how
much flow can go through the graph. If the edge (u, v) is not in E, then
c(u, v) = 0

f(u, v) is the flow through the edge, a non-negative quantity which
represents the traffic through that edge.

f(u, v) obey the following properties:

f(v, v) = 0 forall v in V
f(u, v) = -f(v, u) forall u, v in V (skew symmetry)

The total flow through the network |f| is given by

|f| = sum([f(s, u) for u in V]) = f(s, V) (partial summation notation)

it follows that

f(X, Y) = -f(Y, X) forall subsets X, Y of V
f(union(X, Y), Z) = f(X, Z) + f(Y, Z) - f(intersection(X, Y), Z)
|f| = f(V, t)

A residual network is G_f(V, E_f) is another type of graph representation
of a flow network with the function c_f: V x V -> R defined as

c_f(u, v) = c(u, v) - f(u, v)

Note that if c(v, u) is 0 then c_f(v, u) = -f(v, u) = f(u, v).

Below is a class that will be used as a data structure representing
a residual flow network which will be used for finding the maximum
flow allowable through a flow network.

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
    frontier = [self.src] # queue
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
