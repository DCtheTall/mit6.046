"""
Lecture 20: Asynchronous Distributed Algorithms
Extended Distributed Bellman Ford
Synchronous Distributed Algorithm
---------------------------------
This lecture covers asynchronous distributed
algorithms. A foundation for the algorithm
is an extension of the distributed Bellman-Ford
algorithm from lecture 19.

This implementation will also have each node
keep track of its children nodes in the spanning
tree. In order to do this, each node must send a
"parent" or "non-parent" response to the node
that sent the distance message. When a node receives
a "parent" response, it adds the node that sent
the response to its children set.

In this program, we will assume the network does
not have the number of nodes in the network available.
So in order for the algorithm to terminate, we
need to implement a convergecast strategy like the
BFST algorithm from lecture 19. When each node
receives no "parent" responses from its neighbors, it
guesses it is a leaf node, and sends a "done" message
to its parent. Every non-leaf node will send a "done"
message when all of it's children send a "done" message.
The algorithm terminates when the source vertex is
marked as done.

"""


PARENT = 'parent'
NON_PARENT = 'non-parent'


class Node(object):
  """
  Node object represents a single process
  in the network. It stores internal
  state and has methods which process
  messages from its channels to compute
  the next state

  """
  def __init__(self, uid):
    self.channels = dict()
    self.children = set()
    self.children_done = set()
    self.distance = float('inf')
    self.is_done = False
    self.parent = None
    self.uid = uid

  def handle_distance_msg(self, src_uid, distance):
    """
    This method handles when a
    node receives a "distance" message
    from one of its channels

    """
    c = self.channels[src_uid]
    if self.distance > distance:
      self.distance = distance
      self.is_done = False
      self.parent = src_uid
      self.children = set()
      self.children_done = set()
      c.send_parent_resp(self, PARENT)
    else:
      c.send_parent_resp(
        self, PARENT if src_uid == self.parent else NON_PARENT)

  def handle_done_msg(self, src_uid):
    """
    This method handles when the node
    receives a "done" message from
    one of its children. It since it is not
    a leaf node it must wait for all of its
    children to send a "done" message before
    emitting a "done" message itself

    """
    if self.is_done:
      return
    self.children_done.add(src_uid)
    if self.children_done == self.children:
      self.is_done = True
      for c in map(self.channels.get, self.channels):
        c.send_done_msg(self)

  def handle_parent_resp(self, src_uid, msg):
    """
    This method handles when the node
    receives a "parent" or "non-parent"
    response after sending a "distance"
    message across its channels

    """
    if msg == PARENT:
      self.children.add(src_uid)
    elif src_uid in self.children:
      self.children.remove(src_uid)
      if src_uid in self.children_done:
        self.children_done.remove(src_uid)

  def print_result(self):
    """
    Ouput the resulting state of the node after
    running the algorithm.

    """
    print '{}: parent: {}, distance: {}, children: {}\n'.format(
      self.uid,
      self.parent,
      self.distance,
      sorted(self.children),
    )


class Channel(object):
  """
  Channel class represents a
  connection between two nodes in
  the network

  """
  def __init__(self, u, v, cost):
    self.nodes = (u, v)
    self.cost = cost

  def send_distance_msg(self, src):
    """
    Emit the "distance" message from
    the source node to the other end of
    the channel

    """
    u, v = self.nodes
    dst = v if src == u else u
    dst.handle_distance_msg(src.uid, self.cost + src.distance)

  def send_done_msg(self, src):
    """
    Emit the "done" message from
    the source node to the other end
    of the channel

    """
    u, v = self.nodes
    dst = v if src == u else u
    dst.handle_done_msg(src.uid)

  def send_parent_resp(self, src, msg):
    """
    Emit a "parent" or "non-parent" response
    from the source node to the other end
    of the channel

    """
    u, v = self.nodes
    dst = v if src == u else u
    dst.handle_parent_resp(src.uid, msg)


class Network(object):
  """
  Network object represents a synchronozied
  distributed network of nodes connected
  through two-way channels

  """
  def __init__(self):
    self.nodes = dict()

  def add_node(self, uid):
    """
    Add a node with the provided uid to the
    network

    """
    self.nodes[uid] = Node(uid)

  def add_channel(self, uid_u, uid_v, cost):
    """
    Add a channel between two nodes in the
    network

    """
    u, v = self.nodes[uid_u], self.nodes[uid_v]
    c = Channel(u, v, cost)
    u.channels[v.uid] = c
    v.channels[u.uid] = c

  def execute_round(self):
    """
    Execute one round of message exchanging
    Each node sends a "distance" message across
    each of its channels. A node whose children all
    send a "done" message also emits a "done"
    message across all its channels to inform
    its parent

    """
    for u in self.nodes.values():
      for c in u.channels.values():
        c.send_distance_msg(u)
      if u.children == u.children_done:
        u.is_done = True
        c.send_done_msg(u)


def convergecast_bellman_ford(network, src_uid):
  """
  Bellman-Ford shortest path algorithm for synchronized
  distributed networks. This implementation uses a
  convergecast strategy to signal termination.

  """
  if not isinstance(network, Network):
    raise TypeError(
      'The first argument of convergecast_bellman_ford_shortest_path must be an instance of Network')
  src = network.nodes[src_uid]
  src.distance = 0
  while not src.is_done:
    network.execute_round()
  for u in sorted(network.nodes.values()):
    u.print_result()
