"""
Lecture 7: Randomization
Skip Lists
----------
Skip lists are a randomized linked-list like data structure
that support search in logarithmic time with high probability.

"""


from random import getrandbits


class ListNode(object):
  """
  Skip-list linked list node

  """
  def __init__(self, val):
    self.val = val
    self.next = None
    self.up = None
    self.down = None


class SkipList(object):
  """
  Skip list implementation

  """
  def __init__(self):
    self.levels = [ListNode(-float('inf'))]

  def insert(self, val, level=0):
    """
    Insert into a skip list, promoting
    elements to the higher levels using
    a random coin flip

    """
    curr = self.levels[level]
    node = ListNode(val)
    while curr.next is not None:
      curr = curr.next
      if curr.next is not None \
        and curr.next.val >= val:
          break
    if curr.next is None:
      curr.next = node
    else:
      tmp = curr.next
      curr.next = node
      node.next = tmp
    if getrandbits(1): # random coinflip determines if we insert at the next level
      next_level = level + 1
      if next_level == len(self.levels):
        new_start = ListNode(-float('inf'))
        self.levels[-1].up = new_start
        new_start.down = self.levels[-1]
        self.levels.append(new_start)
      next_level_node = self.insert(val, next_level)
      node.up = next_level_node
      next_level_node.down = node
    return node

  def delete(self, val, level=0):
    """
    Delete a node from the skip list

    """
    curr = self.levels[level]
    while curr.next is not None \
      and curr.next.val != val:
        curr = curr.next
    if curr.next is None: # element not in the list
      return
    tmp = curr.next
    curr.next = curr.next.next
    if tmp.up is not None:
      self.delete(val, level + 1)

  @staticmethod
  def search_list(val, node):
    """
    Static method searches a level of the list
    for the value, if it does not find it it
    recursively will check if the level below
    contains the node, provided a level below exists

    """
    while node.next is not None \
      and node.next.val < val:
        node = node.next
    if node.next is not None \
      and node.next.val == val:
        return True
    if node.down is None:
      return False
    return SkipList.search_list(val, node.down)

  def search(self, val):
    """
    Instance method calls the static search
    method defined above using the top level
    as a starting point

    """
    return SkipList.search_list(val, self.levels[-1])
