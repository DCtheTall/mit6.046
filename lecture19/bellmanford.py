"""
Lecture 19: Synchronized Distributed Algorithms
Bellman-Ford Shortest Path Algorithm
------------------------------------
This lecture is the first on distributed algorithms,
algorithms which are executed on a network of machines
or processors that store memory.

For simplicity, the algorithm implementations in this
repo for synchronous distributed algorithms will be
executed on a single processor using a set of custom
classes meant to mock a network of machines.

This program covers the Bellman-Ford shortest path
distributed algorithm. Let's say we are given a network
of nodes which can communicate through channels,
each with a non-negative cost associated with sending
a message. The goal of the algoirthm is to find the lowest
possible cost it takes to send a message from a provided
source vertex to each node in the network.

The Bellman-Ford algorithm achieves this by having each
pair of connected nodes, u and v, send their urrent distance
(i.e. the cost of sending a message from the source to said
vertex) to each other, and for both vertices

if d(s, u) > d(s, v) + w(v, u) (variables can be interchanged)

then we set node u's "distance" to from s to be

d(s, v) + w(v, u)

this process is called relaxing the edges in the graph
from the source vertex s to u.

The network sends n rounds of messages (recall n = |V|
if the network is the graph G(V, E)) and by the
end, each node's "distance" will be minimized.

"""


class Node(object):
  """
  Node class represents an individual node
  in the network

  """
  def __init__(self, uid):
    self.uid = uid
    self.distance = float('inf')
    self.parent = None

  def receive_distance_msg(self, uid, distance):
    """
    The node receives a message from its neighbor
    with the neighbor's total distance from the
    source vertex plus the cost of sending a message
    through the channel.

    """
    if self.distance > distance:
      distance = self.distance
      self.parent = uid

  def print_result(self):
    """
    Print the node's uid, distance
    from source, and parent uid.

    """
    return '{}: distance: {} parent: {}'.format(
      self.uid,
      self.distance,
      self.parent,
    )


class Channel(object):
  """
  Channel class represents a connection
  between two nodes in the network with
  a non-negative cost of sending a message
  through that channel.

  """
  def __init__(self, u, v, cost):
    self.nodes = (u, v)
    self.cost = cost

  def send_distance_msg(self):
    """
    Have the nodes in the channel
    exchange their distance from
    the source vertex with each
    other.

    """
    u, v = self.nodes
    u.receive_distance_msg(v.uid, v.distance + self.cost)
    v.receive_distance_msg(u.uid, u.distance + self.cost)


class Network(object):
  """
  Network class represents a synchronized
  distributed network of nodes.

  """
  def __init__(self):
    self.nodes = dict()
    self.channels = []

  def add_node(self, uid):
    """
    Add a node to the network.

    """
    self.nodes[uid] = Node(uid)

  def add_channel(self, uid_u, uid_v, cost):
    """
    Create a channel between 2 nodes in the
    network.

    """
    u, v = self.nodes[uid_u], self.nodes[uid_v]
    self.channels.append(Channel(u, v, cost))


def bellman_ford(network, src_uid):
  """
  Bellman-ford shortest path algorithm for
  a synchronized distributed network.

  Complexity:
  Number of messages per round: O(E) = O(n ** 2)
  Number of rounds of messages: O(V) = O(n)

  where G(V, E) is the undirected graph
  representing the network.

  """
  if not isinstance(network, Network):
    raise TypeError(
      'argument of bellman_ford_shortest_path must be a Network instance')
  network.nodes[src_uid].distance = 0
  n = len(network.nodes)
  for _ in range(n - 1):
    for c in network.channels:
      c.send_distance_msg()
  for u in network.nodes:
    u.print_result()
