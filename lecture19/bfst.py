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
    self.neighbor_uids = []
    self.uid = uid
    self.visited = False

  def handle_search_msg(self, src_uid):
    if self.visited:
      self.channels[src_uid].send_parent_resp(NON_PARENT)
    else:
      self.visited = True
      self.parent = src_uid
      self.searching = True
      self.channels[src_uid].send_parent_resp(PARENT)


class Channel(object):
  def __init__(self, u, v):
    self.nodes = (u, v)

  def send_done_msg(self, src):
    u, v = self.nodes
    if u == src:
      v.done = True
    else:
      u.done = True

  def send_parent_resp(self, src, msg):
    u, v = self.nodes
    if u == src:
      v.is_parent = msg == PARENT
    else:
      u.is_parent = msg == PARENT

  def send_search_message(self, src):
    u, v = self.nodes
    if u == src:
      v.handle_search_msg(src.uid)
    else:
      u.handle_search_msg(src.uid)
