"""
PriorityQueue for Prim's algorithm
----------------------------------

Prim's algorithm requires you maintain
a priority queue which can update the priority
of each vertex

"""


from random import sample


class PriorityQueue(object):
  """
  PriorityQueue which has the ability to update the
  value of a key, and pop the key with the minimum
  value.

  The efficiency of this can be improved if you
  use a vEB tree as the underlying data structure
  for large graphs.

  """

  def __init__(self, graph):
    src = sample(graph.vertices, 1)
    self.data = {
        u: 0 if u == src else float('inf')
        for u in graph.vertices
    }

  def is_empty(self):
    """
    Returns if queue is empty

    """
    return len(self.data) == 0

  def contains(self, key):
    """
    Returns a bool representing if key is in the queue

    """
    return key in self.data

  def pop_min(self):
    """
    Pop key with minimum priority in O(n) time

    """
    u = min(self.data, key=self.data.get)
    del self.data[u]
    return u

  def update(self, key, val):
    """
    Update the priority (val) of a key in the queue

    """
    self.data[key] = val
