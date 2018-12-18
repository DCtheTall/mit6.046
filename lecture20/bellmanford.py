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
  def __init__(self, uid):
    self.channels = dict()
    self.children = set()
    self.children_done = set()
    self.distance = float('inf')
    self.is_done = False
    self.parent = None
    self.uid = uid

  def handle_distance_msg(self, src_uid, distance):
    c = self.channels[src_uid]
    if self.distance > distance:
      self.distance = distance
      self.is_done = False
      self.parent = src_uid
      self.children = set()
      self.children_done = set()
      c.send_parent_resp(self.uid, PARENT)
    else:
      c.send_parent_resp(self.uid, NON_PARENT)


class Channel(object):
  def __init__(self, u, v, cost):
    self.nodes = (u, v)
    self.cost = cost

  def send_parent_resp(self, src_uid, msg):
    pass
