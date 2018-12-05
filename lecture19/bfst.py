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
    self.done = False
    self.is_parent = False
    self.parent = None
    self.searching = False
    self.uid = uid
    self.visited = False

  def handle_done_message(self):
    if not self.done:
      self.done = True
      for c in map(self.channels.get, self.channels):
        c.send_done_msg(self)

  def handle_search_msg(self, src_uid):
    self.searching = False
    if self.visited:
      self.channels[src_uid].send_parent_resp(self, NON_PARENT)
    else:
      self.parent = src_uid
      self.searching = True
      self.visited = True
      self.channels[src_uid].send_parent_resp(self, PARENT)

  def print_result(self):
    print '{}: parent: {}'.format(self.uid, self.parent)


class Channel(object):
  def __init__(self, u, v):
    self.nodes = (u, v)

  def send_done_msg(self, src):
    u, v = self.nodes
    if u == src:
      v.handle_done_message()
    else:
      u.handle_done_message()

  def send_parent_resp(self, src, msg):
    u, v = self.nodes
    dst = v if src == u else u
    dst.is_parent = msg == PARENT

  def send_search_message(self, src):
    u, v = self.nodes
    dst = v if src == u else u
    dst.handle_search_msg(src.uid)
    if not dst.is_parent:
      self.send_done_msg(dst)


class Network(object):
  def __init__(self):
    self.nodes = dict()
    self.channels = []

  def add_node(self, uid):
    self.nodes[uid] = Node(uid)

  def add_channel(self, uid_u, uid_v):
    u, v = self.nodes[uid_u], self.nodes[uid_v]
    c = Channel(u, v)
    self.channels.append(c)
    u.channels[v.uid] = c
    v.channels[u.uid] = c

  def execute_round(self):
    cur_round = set()
    for c in self.channels:
      u, v = c.nodes
      if u.searching:
        c.send_search_message(u)
        cur_round.add(u.uid)
      elif v.searching:
        c.send_search_message(v)
        cur_round.add(v.uid)
    for uid in cur_round:
      self.nodes[uid].searching = False


def breadth_first_spanning_tree(network, src_uid):
  if not isinstance(network, Network):
    raise TypeError(
      'argument of breadth_first_spanning_tree must be an instance of Network')
  src = network.nodes[src_uid]
  src.searching = True
  src.visited = True
  while not src.done:
    network.execute_round()
  for u in map(network.nodes.get, network.nodes):
    u.print_result()
