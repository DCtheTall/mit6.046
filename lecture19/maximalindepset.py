"""
Lecture 19: Synchronous Distributed Algorithms
Luby's Maximal Independent Set Algorithm
----------------------------------------
This lecture is the first on distributed algorithms,
algorithms which are executed on a network of machines
or processors that store memory.

For simplicity, the algorithm implementations in this
repo for synchronous distributed algorithms will be
executed on a single processor using a set of custom
classes meant to mock a network of machines.

This program covers maximal indepdendent set algorithm.
Given an undirected graph G(V, E) representing a network
of nodes of size n = |V|, a maximal independent set (MIS)
is a subset of V, let's call it S, such that

1. No two vertices in S are adjacent (independence).
2. Adding any other vertex in V that is not in S
  will create a new set that violates the
  independence property (maximality).

This program has an implementation of a Luby's MIS
algorithm, a probabilistic algorithm covered in
lecture:

1.  Each node starts as being marked as "active."

2.  Each round, each active node generates a unique
    ID from 1 to n ** 5 (recall n = |V| = number of
    nodes). Each active node then exchanges its uid
    with each of its active neighbors.

3.  If a node's uid is strictly greater than all of
    its neighbors uid, this node will output it
    is IN the MIS. It is marked as inactive and
    then sends an "in MIS" message to each of its
    neighbors. Its neighbors then output they are
    OUT of the MIS, and they are marked as inactive.

The algorithm continues until all nodes are
marked as inactive.

"""


from random import randint


IN = 'IN'
OUT = 'OUT'


class Node(object):
  """
  Node class for representing a node
  in this network for the MIS algorithm.

  The node's "key" is the key the Network
  class stores each Node instance in a
  dictionary.

  The uid is the random unique ID generated
  each round for the algorithm to determine
  the maximal independent subset.

  """
  def __init__(self, key):
    self.active = True
    self.in_mis = None
    self.key = key
    self.uid = None
    self.neighbors_uids = []
    self.channels = []

  def receive_in_mis(self):
    """
    This method is for handling when a node
    receives a message from its neighbor
    that the neighbor is in the MIS

    """
    self.in_mis = OUT
    self.active = False

  def receive_uid(self, uid):
    """
    Receive an instance of NodeState
    from a data channel

    """
    self.neighbors_uids.append(uid)

  def receive_result_of_round(self):
    """
    Handle a round of the algorithm after
    a uid has been randomly assigned and
    messages between active nodes have
    been sent.

    """
    max_uid = max(self.neighbors_uids)
    if self.uid > max_uid:
      self.in_mis = IN
      self.active = False
      for c in self.channels:
        c.send_in_mis(self)


class Channel(object):
  """
  Channel object represents an edge
  in the graph representation of the
  network. It is a two way channel
  through which each node can send
  messages to its pair.

  """
  def __init__(self, u, v):
    self.nodes = (u, v)

  def exchange_uids(self):
    """
    Have the two nodes at either end of the
    channel exchange uids.

    """
    u, v = self.nodes
    v.receive_uid(u.uid)
    u.receive_uid(v.uid)

  def send_in_mis(self, u):
    """
    Have the node u send that it is
    in the maximal independent subset
    to its neighbor on the other end
    of the channel.

    """
    v, w = self.nodes
    if u == v:
      w.receive_in_mis()
    else:
      v.receive_in_mis()


class Network(object):
  """
  Network class is a representation
  of a synchronized network using
  Node instances for vertices and
  Channel instances for edges.

  """
  def __init__(self):
    self.nodes = dict()
    self.channels = []

  def add_channel(self, u_key, v_key):
    """
    Add a channel between nodes at the
    specified key

    """
    u, v = self.nodes[u_key], self.nodes[v_key]
    c = Channel(u, v)
    u.channels.append(c)
    v.channels.append(c)
    self.channels.append(c)

  def add_node(self, key):
    """
    Add a node to the network and
    give it the unique id "key"

    """
    self.nodes[key] = Node(key)

  def execute_round(self):
    """
    Execute a round of the MIS algorithm.
    Each active node generates a unique
    id from 1 to n ** 5. Each channel
    where both nodes are active exchanges
    its nodes' uids. The node then computes
    the new state after the transmission
    is complete.

    """
    should_continue = False
    n = len(self.nodes)
    for u in self.nodes.values():
      if u.active:
        u.uid = randint(1, n ** 5)
    for c in self.channels:
      u, v = c.nodes
      if u.active and v.active:
        c.exchange_uids()
    for u in self.nodes.values():
      if u.active:
        u.receive_result_of_round()
      should_continue |= u.active
    return should_continue

  def output_result(self):
    """
    Outputs if each node is in the MIS
    in the order of their keys in the
    dictionary.

    """
    for u in map(
      self.nodes.get, sorted(self.nodes.keys())):
        print u.in_mis


def luby_maximal_independent_subset(network):
  """
  Maximal indendent subset synchronized
  distributed algorithm.

  An implementation of the MIS algorithm
  from lecture using the objects defined
  above.

  Complexity:

  Number of message: O(V + E) = O(n ** 2)
  Number of rounds: O(4 * log(n)) (with probability 1 - (1 / n))

  """
  if not isinstance(network, Network):
    raise TypeError(
      'argument of maximal_independent_subset must be an instance of Network')
  should_continue = network.execute_round()
  while should_continue:
    should_continue = network.execute_round()
  network.output_result()
