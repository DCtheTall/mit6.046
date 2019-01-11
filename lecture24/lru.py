"""
Lecture 24: Cache-Oblivious Algorithm
LRU Cache
---------
An LRU Cache is a cache which, when full, deletes
the object which was accessed least recently, hence
the name "least recently used cache."

The implementation below is a solution to LeetCode problem
146, which is to implement an LRU cache.

"""


class ListNode(object):
  """
  ListNode class is used as a node
  in a doubley linked list that is used
  to keep track of the order in which
  nodes were accessed.

  """
  def __init__(self, key):
    self.key = key
    self.next = self.prev = None


class LRUCache(object):
  """
  LRU Cache object uses a doubley-linked
  list to perform insertion and deletion
  in O(1) time.

  """
  def __init__(self, capacity):
      self.C = capacity
      self.D = dict()
      self.L = dict()
      self.head = self.tail = None

  def move_to_back(self, key):
    """
    Move the list node for the specified
    key to the back of the linked list, meaning
    it will be deleted last.

    """
    cur = self.L[key]
    if cur == self.tail:
      return
    if cur == self.head:
      self.head = cur.prev
    if cur.prev is not None:
      cur.prev.next = cur.next
    if cur.next is not None:
      cur.next.prev = cur.prev
    cur.prev = None
    cur.next = self.tail
    self.tail.prev = cur
    self.tail = cur

  def get(self, key):
    """
    Key the value stored at a key in the cache. If the key is
    not in the cache, return None.

    """
    if key in self.D:
      self.move_to_back(key)
      return self.D[key]
    return None

  def put(self, key, value):
    """
    Put a value into the cache at the given key. If the
    key is already in the cache, update the value and then
    update the doubley linked list. If the cache is full,
    pop the tail of the list and delete the value at that key.

    """
    if key in self.D:
      self.D[key] = value
      self.move_to_back(key)
      return
    if self.C == 1:
      self.head = self.tail = None
      self.D = dict()
      self.L = dict()
    if len(self.D) == self.C:
      del self.D[self.head.key]
      del self.L[self.head.key]
      self.head.prev.next = None
      self.head = self.head.prev
    self.L[key] = ListNode(key)
    self.D[key] = value
    if self.tail is not None:
      self.tail.prev = self.L[key]
      self.L[key].next = self.tail
    if self.head is None:
      self.head = self.L[key]
    self.tail = self.L[key]
