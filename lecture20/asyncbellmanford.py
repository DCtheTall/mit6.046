"""
Lecture 20: Asynchronous Distributed Algorithms
Asynchronous Bellman-Ford Shortest Paths
----------------------------------------
This program is an implementation of the Bellman-Ford
shortest path algorithm on a an asynchronous network
of nodes where each channel between nodes has a non-negative
"cost" of sending a message. The algorithm
converges when each nodes has found the minimum cost
of sending a message from a chosen source node.

This algorithm is similar to the asynchronous
breadth-first spanning tree algorithm in
lecture20/asyncbfst.py, only once a node is
visited, it may still find a better path and emit
more messages.

In this algorithm, are minimizing the distance of
each node from the source vertex. Since each message
cost is always greater than or equal to 0, an optimal
path always exists between two nodes. So convergence
is guaranteed for all asynchronous networks.

"""


from collections import deque


class Node(object):
  """
  Node object represents a single process
  in the asynchronous network.

  """
  def __init__(self, key):
    self.channels = []
    self.distance = float('inf')
    self.key = key
    self.parent = None

  def emit_msg(self):
    """
    Emit a message with its current distance from
    the source vertex across all channels.

    """
    for c in self.channels:
      c.enqueue_msg(self)

  def receive_msg(self, key, distance):
    """
    Handles when this node receives a message
    from one of its channels.

    """
    if distance < self.distance:
      self.parent = key
      self.distance = distance
      self.emit_msg()


class Channel(object):
  """
  Channel object represents a channel of
  communication between two nodes in the
  network. It has a non-negative "cost"
  of sending messages associated with it.

  """
  def __init__(self, u, v, cost):
    self.cost = cost
    self.mqueue = deque()
    self.nodes = (u, v)

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
    Enqueue a message into the message
    queue.

    """
    u, v = self.nodes
    dst = v if src == u else u
    self.mqueue.append(
        (dst, src.key, src.distance + self.cost))

  def dequeue_msg(self):
    """
    Deliver the message at the head of
    the queue.

    """
    dst, key, distance = self.mqueue.popleft()
    dst.receive_msg(key, distance)


class Network(object):
  """
  Network object represents an asynchronous
  distributed network of processes which share
  channels of communication.

  """
  def __init__(self):
    self.channels = []
    self.nodes = dict()

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
    Add a node to the network.

    """
    self.nodes[key] = Node(key)

  def add_channel(self, u, v, cost):
    """
    Add a channel to the network.

    """
    u, v = self.nodes[u], self.nodes[v]
    c = Channel(u, v, cost)
    self.channels.append(c)
    u.channels.append(c)
    v.channels.append(c)


def async_bellman_ford(network, src):
  """
  Asynchronous Bellman-Ford shortest path
  algorithm from a chosen source vertex.

  It starts by setting the source vertex's
  distance to 0 and then having it emit
  a message across all its channels.

  When nodes get a message from a more optimal
  path than they have seen, they enqueue
  a message in their channels. The algorithm
  continues until the network has no more messages
  to send. The messages do not need to arrive
  at the nodes in any particular order for the
  algorithm to be correct.

  """
  if not isinstance(network, Network):
    raise TypeError(
        'first argument of async_bellman_ford must be an instance of Network')
  network.nodes[src].distance = 0
  network.nodes[src].emit_msg()
  while network.has_queued_messages:
    for c in network.channels:
      if c.has_queued_messages:
        c.dequeue_msg()
  for u in network.nodes.values():
    print '{}: parent: {} distance: {}'.format(
        u.key, u.parent, u.distance)
