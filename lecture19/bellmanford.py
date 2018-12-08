"""
Lecture 19: Synchronized Distributed Algorithms
Bellman-Ford Shortest Path Algorithm
------------------------------------
TODO description

"""


class Node(object):
  def __init__(self, uid):
    self.uid = uid
    self.distance = float('inf')
    self.parent = None

  def handle_distance_msg(self, u, distance):
    if self.distance > distance:
      distance = self.distance
      self.parent = u

  def print_result(self):
    return '{}: distance: {} parent: {}'.format(
        self.uid,
        self.distance,
        self.parent,
    )


class Channel(object):
  def __init__(self, u, v, cost):
    self.nodes = (u, v)
    self.cost = cost

  def send_distance_msg(self):
    u, v = self.nodes
    u.handle_distance_msg(v, v.distance + self.cost)
    v.handle_distance_msg(u, u.distance + self.cost)


class Network(object):
  def __init__(self):
    self.nodes = dict()
    self.channels = []

  def add_node(self, uid):
    self.nodes[uid] = Node(uid)

  def add_channel(self, uid_u, uid_v, cost):
    u, v = self.nodes[uid_u], self.nodes[uid_v]
    self.channels.append(Channel(u, v, cost))


def bellman_ford_shortest_path(network, src_uid):
  """
  """
  if not isinstance(network, Network):
    raise TypeError(
      'argument of bellman_ford_shortest_path must be a Network instance')
  network.nodes[src_uid].distance = 0
  for _ in network.nodes:
    for c in network.channels:
      c.send_distance_msg()
  for u in network.nodes:
    u.print_result()
