"""
Lecture 19: Synchronous Distributed Algorithms
Maximal Independent Set
-----------------------
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

This program has an implementation of a probabilistic
algorithm covered in lecture. Each "active" node

"""


from random import randint


IN = 'IN'
OUT = 'OUT'


class NodeState(object):
  """
  This is a serealizable object
  which represents each network
  node's state during the algorithm.

  The Channel objects exchange instances
  of this object for nodes to communicate
  what their current state in the current
  round of the algorithm is.

  """
  def __init__(self, uid):
    self.active = True
    self.in_mis = None
    self.uid = uid


class Node(object):
  """
  Node class for representing a node
  in this network for the MIS algorithm.
  It contains an instance of NodeState
  representing it own state.

  """
  def __init__(self, uid):
    self.state = NodeState(uid)
    self.neighbors_state = []
    self.channels = []

  def receive_in_mis(self):
    self.state.in_mis = OUT
    self.state.active = False

  def receive_state(self, state):
    """
    Receive an instance of NodeState
    from a data channel

    """
    max_uid = map(
      map(lambda state: state.uid, self.neighbors_state))
    if self.state.uid > max_uid:
      self.state.in_mis = IN
      self.state.active = False
      for c in self.channels:
        c.send_from(self).send_in_mis()


class Channel(object):
  def __init__(self, u, v):
    self.nodes = (u, v)
    self.from_node = None

  def emit_states(self):
    u, v = self.nodes
    u.receive_state(v.state)
    v.receive_state(u.state)

  def send_from(self, u):
      self.from_node = u
      return self

  def send_in_mis(self):
    u, v = self.nodes
    if u == self.from_node:
      v.receive_in_mis()
    else:
      u.receive_in_mis()


class Network(object):
  def __init__(self):
    self.nodes = {}
    self.channels = []

  def add_node(self, uid):
    self.nodes[uid] = Node(uid)

  def add_channel(self, uid_u, uid_v):
    u, v = self.nodes[uid_u], self.nodes[uid_v]
    c = Channel(u, v)
    u.channels.append(c)
    v.channels.append(v)
