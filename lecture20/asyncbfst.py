"""
Lecture 20: Asynchronous Distributed Algorithms
Asynchronous Breadth-First Spanning Tree
----------------------------------------
This program covers an asynchronous algorithm
for find a spanning tree of a network of nodes.
The model for the asynchronous network is covered
in lecture20/asyncleaderelection.py.

The algorithm starts by selecting a root node for
the tree, and have that node enqueue a message
in each of its channels.

Afterwards, each time a node receives a message
and it has not yet been visited, it stores its
distance from the root, its parent, and then
emits a message across all of its channels.

The algorithm converges when there are no
more messages left in any channel's queue.

"""


from collections import deque


class Node(object):
  """
  Node class represents a process in
  the asynchronous distributed network.

  """
  def __init__(self, key):
    self.channels = []
    self.distance = float('inf')
    self.key = key
    self.parent = None
    self.visited = False

  def emit_msg(self):
    """
    Have each of the node's channels
    emit a message.

    """
    for c in self.channels:
      c.enqueue_msg(self)

  def receive_msg(self, key, distance):
    """
    Handles when the node receives
    a message from one of its channels.

    """
    if self.visited:
      return
    self.distance = distance + 1
    self.parent = key
    self.visited = True
    self.emit_msg()


class Channel(object):
  """
  Channel class represents a connection
  between two nodes in the network.

  """
  def __init__(self, u, v):
    self.nodes = (u, v)
    self.mqueue = deque()

  @property
  def has_queued_messages(self):
    """
    A getter to see if the channel
    has any messages in its queue.
    Empty queues type cast to False.

    """
    return bool(self.mqueue)

  def enqueue_msg(self, src):
    """
    Add a message to the channel's
    message queue.

    """
    u, v = self.nodes
    dst = v if src == u else u
    self.mqueue.append((dst, src.key, src.distance))

  def dequeue_msg(self):
    """
    Deliver the message at the
    head of the channel's queue.

    """
    dst, key, distance = self.mqueue.popleft()
    dst.receive_msg(key, distance)


class Network(object):
  """
  Network class representing an
  asynchronous distributed network
  of processes.

  """
  def __init__(self):
    self.nodes = dict()
    self.channels = []

  @property
  def has_queued_messages(self):
    """
    A getter to see if any channel
    in the network has messages left
    in their queues to send.

    """
    return any(map(
        lambda c: c.has_queued_messages,
        self.channels))

  def add_node(self, key):
    """
    Add a node to the network

    """
    self.nodes[key] = Node(key)

  def add_channel(self, u, v):
    """
    Add a channel to the network

    """
    u, v = self.nodes[u], self.nodes[v]
    c = Channel(u, v)
    self.channels.append(c)
    u.channels.append(c)
    v.channels.append(c)


def async_bfst(network, src):
  """
  Asynchronous bread-first spanning
  tree algorithm using the classes
  above to represent an asynchronous
  distributed network.

  """
  if not isinstance(network, Network):
    raise TypeError(
        'first argument of async_bfst must be an instance of Network')
  src = network.nodes[src]
  src.visited = True
  src.distance = 0
  src.emit_msg()
  while network.has_queued_messages:
    for c in network.channels:
      if c.has_queued_messages:
        c.dequeue_msg()
  for u in network.nodes.values():
    print '{}: parent: {} distance: {}'.format(
        u.key, u.parent, u.distance)
