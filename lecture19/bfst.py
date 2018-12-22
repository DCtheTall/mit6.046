"""
Lecture 19: Synchronized Distributed Algorithms
Breadth-First Spanning Tree
---------------------------
This lecture is the first on distributed algorithms,
algorithms which are executed on a network of machines
or processors that store memory.

For simplicity, the algorithm implementations in this
repo for synchronous distributed algorithms will be
executed on a single processor using a set of custom
classes meant to mock a network of machines.

This program covers a distributed algorithm for
computing the spanning-tree of a synchronized
distributed network. The algorithm starts at a
designated node in the network, then it does
a breadth-first search for unvisited nodes and
sets their parent pointers.

"""


PARENT = 'parent'
NON_PARENT = 'non-parent'


class Node(object):
  """
  Node class which has its own unique ID and
  is aware of its neighbords unique IDs, uses
  neighbors IDs as keys for the channel
  connecting them in the `channels` dictionary.

  """
  def __init__(self, uid):
    self.channels = dict()
    self.children = set()
    self.children_done = set()
    self.distance = float('inf')
    self.is_done = False
    self.is_parent = False
    self.parent = None
    self.searching = False
    self.uid = uid
    self.visited = False

  def receive_done_msg(self, child_uid):
    """
    Compute the node's state after
    it receives a done message from one
    of its children. If the node is not
    yet marked as "done" and all of its
    children are marked "done", then it
    sends a "done" message across all
    of its channels

    """
    if self.is_done:
      return
    self.children_done.add(child_uid)
    if self.children == self.children_done:
      self.is_done = True
      for c in self.channels.values():
        c.send_done_msg(self)


  def receive_parent_resp(self, src_uid, msg):
    """
    Compute the node's state when it receives
    a "is parent" response from a node after
    sending a "search" message

    """
    if msg == PARENT:
      self.children.add(src_uid)

  def receive_search_msg(self, src_uid, dist):
    """
    Compute the node's state when it receives
    a "search" message from one of its neighbors.

    """
    if self.visited:
      self.channels[src_uid].send_parent_resp(self, NON_PARENT)
    else:
      self.distance = dist + 1
      self.parent = src_uid
      self.searching = True
      self.visited = True
      self.channels[src_uid].send_parent_resp(self, PARENT)

  def print_result(self):
    """
    Ouput the resulting state of the node after
    running the BFST algorithm.

    """
    print '{}: parent: {}, distance: {}, children: {}\n'.format(
      self.uid,
      self.parent,
      self.distance,
      sorted(self.children),
    )


class Channel(object):
  """
  Channel class is an object meant to
  simulate a connection between nodes
  in a synchronized distributed network.
  They are used as the edges of the
  graph representation of the network.

  """
  def __init__(self, u, v):
    self.nodes = (u, v)

  def send_done_msg(self, src):
    """
    Send a "done" message from the source node
    to the other end of the channel

    """
    u, v = self.nodes
    dst = v if src == u else u
    dst.receive_done_msg(src.uid)

  def send_parent_resp(self, src, msg):
    """
    Send a "is parent" response from the source node
    to the other end of the channel, this message
    indicates to the destination node that it is or
    is not the parent of this node in the tree.

    """
    u, v = self.nodes
    dst = v if src == u else u
    dst.receive_parent_resp(src.uid, msg)

  def send_search_message(self, src):
    """
    Sends the "search" message from the source node
    to the other end of the channel

    """
    src.seaching = False
    u, v = self.nodes
    dst = v if src == u else u
    dst.receive_search_msg(src.uid, src.distance)


class Network(object):
  """
  Network class is a graph representation
  of a synchronized distributed network

  """
  def __init__(self):
    self.nodes = dict()

  def add_node(self, uid):
    """
    Add a node to the network

    """
    self.nodes[uid] = Node(uid)

  def add_channel(self, uid_u, uid_v):
    """
    Add a channel between existing nodes

    """
    u, v = self.nodes[uid_u], self.nodes[uid_v]
    c = Channel(u, v)
    u.channels[v.uid] = c
    v.channels[u.uid] = c

  def execute_round(self):
    """
    Execute a round of the BFST algorithm for
    synchronized distributed networks.

    """
    for u in self.nodes.values():
      if u.searching:
        for c in u.channels.values():
          c.send_search_message(u)
        if len(u.children) == 0:
          u.is_done = True
          for c in u.channels.values():
            c.send_done_msg(u)


def breadth_first_spanning_tree(network, src_uid):
  """
  Breadth-First Spanning Tree algorithm
  covered in lecture for a synchronized
  distributed network.

  The first round of the algorithm, the source
  node (root of the tree) sends a "search" message
  to each of its channels. Each node is sends a
  "is parent" response to the source vertex, marks
  itself as "visited" and "searching" and
  the algorithm continues to the next round

  For each subsequent round, the nodes marked as
  "searching" sends a "search" message to their
  neighbors and the neighbors handle the "search"
  message the same way as the nodes in the first
  round.

  This algorithm continues until it reaches only
  leaf nodes. Leaf nodes are nodes that send "search"
  messages and after collecting "is parent" responses
  is not a parent to any node. They then instruct
  their parents to propagate a "done" message up the
  parent pointer chain until the source node is marked
  as "done".

  Complexity:
  Number of messages per round: O(V + E) = O(n ** 2)
  Number of rounds for algo: O(V) = O(n)

  """
  if not isinstance(network, Network):
    raise TypeError(
      'argument of breadth_first_spanning_tree must be an instance of Network')
  src = network.nodes[src_uid]
  src.searching = True
  src.visited = True
  src.distance = 0
  while not src.is_done:
    network.execute_round()
  for u in network.nodes.values():
    u.print_result()
