"""
Lecture 19: Synchronous Distributed Algorithms
Leader Election
---------------
This lecture is the first on distributed algorithms,
algorithms which are executed on a network of machines
or processors that store memory.

For simplicity, the algorithm implementations in this
repo for synchronous distributed algorithms will be
executed on a single processor using a set of custom
classes meant to mock a network of machines.

This program covers leader election, a simple distributed
algorithm where a network of nodes select a leader. In
this case, the nodes are represented using a complete,
undirected graph, called a clique network.

This program covers two methods for selecting a leader
in a complete network of nodes:

1. A deterministic algorithm for selecting a leader in a
  clique network of nodes with unique ids. Each node in
  the netowrk already has a unique id. Each node in the
  network sends each other their ids, and the node with
  the maximum id outputs LEADER, the rest output FOLLOWER.

2. A probabilistic algorithm for selecting a leader in a
  clique network of nodes with no unique ids, instead each
  id is assigned randomly such that there is a high probability
  that no two nodes share an id, and a leader is selected
  using the same process as the deterministic algorithm. If
  two nodes were randomly assigned the same maximum id, then
  the algorithm reassigns ids and continues until a maximum
  id is found.

"""


from random import randint


class Node(object):
  """
  Node class for representing a network node
  each node is aware of only its own unique
  id and the channels to its neighbors.

  Each node starts not knowing the uid of its
  neighbors, but after one round of either
  algorithm, the node learns its neighbors
  ids

  """
  def __init__(self, uid=None):
    self.neighbors_uids = []
    self.uid = uid

  def receive_uid(self, uid):
    """
    Receive a uid message from a data
    channel when a message is emitted.

    """
    self.neighbors_uids.append(uid)

  def output_is_leader(self):
    """
    Outputs if the node is the leader or not.
    For this simple example, it prints to the console
    if it is the leader or a follower node.

    """
    max_uid = max(self.neighbors_uids)
    if self.uid == max_uid:
      raise Exception('Duplicate max uid')
    elif self.uid > max_uid:
      print 'LEADER'
    else:
      print 'FOLLOWER'


class Channel(object):
  """
  Channel class represents a data channel
  between two nodes in the network

  """
  def __init__(self, u, v):
    self.nodes = (u, v)

  def emit_message(self):
    """
    Emit a message from one node to another across
    data channels. For this example, it sends a
    two-way message where the nodes exchange uids

    """
    u, v = self.nodes
    u.receive_uid(v.uid)
    v.receive_uid(u.uid)


class CliqueNetwork(object):
  """
  CliqueNetwork class is meant to be a
  simplified representation of a synchronized
  distributed network.

  The network is represented using an undirected
  complete graph where each vertex is an instance
  of the Node class and each edge is an instance
  of the Channel class.

  """
  def __init__(self):
    self.nodes = []
    self.channels = []

  def add_node(self, u):
    """
    Add a node to a network and create
    a channel from every existing node
    to the new one.

    """
    for v in self.nodes:
      self.channels.append(Channel(u, v))
    self.nodes.append(u)

  def execute_round(self):
    """
    Emit a two-way message across each channel
    in the network. In this case each node emits
    their id to one another.

    """
    for c in self.channels:
      c.emit_message()

  def output_result(self):
    """
    Output the result of the leader election
    from each node in the network

    """
    for u in self.nodes:
      u.output_is_leader()


def deterministic_elect_leader(network):
  """
  Deterministic algorithm for choosing a leader
  node in a synchronized distributed network
  uses methods defined in the CliqueNetwork class
  all nodes should ouput FOLLOWER except the last
  added.

  Complexity:

  Number of rounds: O(1)
  Number of messages: O(n ** 2)

  """
  if not isinstance(network, CliqueNetwork):
    raise TypeError(
      'first argument of deterministic_leader_election must be an instance of CliqueNetwork')
  network.execute_round()
  network.output_result()


def ceil(a, b):
  """
  Returns the ceiling of a on b

  """
  c = float(a) / float(b)
  if c == int(c):
    return int(c)
  return int(c) + 1


def probabilistic_elect_leader(network, epsilon):
  """
  Probabilistic algorithm for leader election in a network
  of nodes. In this case, uids are not assigned before
  the call (if they are they are overwritten) with a random
  set of keys from 1 to upper_bound where

  upper_bound = ceil(n ** 2, (2 * epsilon))

  Recall for distributed networks n = |V| where G(V, E)
  is the graph representation.

  It is shown in lecture notes it is guaranteed to
  produce a unique maximum with
  probability.

  1 - epsilon

  Number of rounds: O(1)
  Number of messages: O(n ** 2)

  """
  if not isinstance(network, CliqueNetwork):
    raise TypeError(
      'first argument of deterministic_leader_election must be an instance of CliqueNetwork')
  n = len(network.nodes)
  upper_bound = ceil(n ** 2, (2 * epsilon))
  for u in network.nodes:
    u.uid = randint(1, upper_bound)
  network.execute_round()
  try:
    network.output_result()
  except:
    print 'Failed to elect leader. Retrying...'
    for u in network.nodes:
      u.data = []
    probabilistic_elect_leader(network, epsilon)
