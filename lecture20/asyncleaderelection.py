"""
Lecture 20: Asynchronous Distributed Networks
Asynchronous Maximum UID Algorithm
----------------------------------
This algorithm is the first example of a asynchronous
distributed algorithm. In the synchronous model, we
assumed each node in the network would emit messages
across each of its channels in synchronized rounds.

In the asynchronous distributed network, channels store
messages in a queue, and each node has the ability to send
messages to be added to the channels queue. The channels
individually then emit the first element in their message
queue to the destination node. The algorithms for asynchronous
distributed networks must converge regardless of
message order.

This program convers asynchronous leader election, where a
network of nodes reaches a consensus on which node has the
greatest key.

The algorithm starts having each node enqueue a message
with its key in all of its channels. Then as the channels
dequeue their messages, when a node received a message
with a key greater than the greatest key the node has seen
so far (starting with just its own key), it stores the
new value and emits messages again across all of its channels.

The algorithm converges when each key learns of the
globally maximum key in the network, and no longer adds
messages to their channels' queue.

"""


from collections import deque


class Node(object):
  """
  This class represents a single process
  in the network. It stores its original
  key, the maximum key it has encountered
  (val) and a list of its channels to
  other nodes.

  """
  def __init__(self, key):
    self.key = key
    self.val = key
    self.channels = []

  def emit_msg(self):
    """
    Emit a message communicating its key
    across all channels.

    """
    for c in self.channels:
      c.enqueue_msg(self)

  def receive_msg(self, key):
    """
    Handles a message from its channel

    """
    if key > self.val:
      self.val = key
      self.emit_msg()


class Channel(object):
  """
  This class represents a connection between
  two nodes in the network.

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
    Add a message from a node to
    the channel queue

    """
    u, v = self.nodes
    dst = v if src == u else u
    self.mqueue.append((dst, src.key))

  def dequeue_msg(self):
    """
    Deliver the message at the
    head of the queue.

    """
    dst, key = self.mqueue.popleft()
    dst.receive_msg(key)


class Network(object):
  """
  A class which implements a theoretical
  model of a asynchronous network of processes
  and channels of communication between
  them.

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
    Add a node to the network.

    """
    self.nodes[key] = Node(key)

  def add_channel(self, u, v):
    """
    Add channel between two nodes.

    """
    u, v = self.nodes[u], self.nodes[v]
    c = Channel(u, v)
    self.channels.append(c)
    u.channels.append(c)
    v.channels.append(c)


def async_leader_election(network):
  """
  Leader election in an asynchronous distributed
  network. The algorithm converges once every
  node has seen the maximum key value and no
  more messages are emitted.

  """
  if not isinstance(network, Network):
    raise TypeError(
        'argument of async_max must be an instance of Network')
  for u in network.nodes.values():
    u.emit_msg()
  while network.has_queued_messages:
    for c in network.channels:
      if c.has_queued_messages:
        c.dequeue_msg()
  for u in network.nodes.values():
    print 'key: {} leader: {}'.format(u.key, u.val)
