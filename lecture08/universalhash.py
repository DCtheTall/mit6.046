"""
Lecture 8: Randomization
Universal Hash Functions
------------------------
An implementation of a hash table with
chaining which uses a universal hash
function

"""


from random import randint


class LinkedListNode(object):
  """
  LinkedListNode is stored at each slot
  in the hash table

  """
  def __init__(self, key, val):
    self.key = key
    self.val = val
    self.next = None


class DotProductHashTable(object):
  """
  Hash table with integer keys
  which uses universal hash function

  Supports set, get, and delete

  m: size of the table, range of the hash function is {0, 1, ..., m - 1}
  u: size of all possible inputs for keys, domain of hash function {0, 1, ..., u - 1}

  param: m {int}
  param: r {int}

  """
  def __init__(self, m, r):
    self.m = m
    self.r = r
    self.u = m ** r
    self.a = randint(0, self.u - 1)
    self.table = [None] * m

  def dot_product_hash(self, key):
    """
    The dot product hash function takes
    the dot product of the coefficients
    of the input, key, and the randomly
    chosen constant, a, both represented
    as polynomials base m, our table size.

    i.e.
    key = k_0 + (k_1 * m) + (k_2 * (m ** 2)) + ... + (a_(r - 1) * (m ** (r - 1)))
    a = a_0 + (a_1 * m) + (a_2 * (m ** 2)) + ... + (k_(r - 1) * (m ** (r - 1)))

    h_a(key) = sum(k_i * a_i for i in range(r)) % m

    """
    key = key % self.u
    a = self.a
    result = 0
    for _ in range(self.r):
      result += (key % self.m) * (a % self.m)
      key //= self.m
      a //= self.m
    return result % self.m

  def set(self, key, val):
    """
    Sets a val to be stored at key,
    if the key is already in the table
    it will overwrite it

    """
    h = self.dot_product_hash(key)
    if self.table[h] is None:
      self.table[h] = LinkedListNode(key, val)
    else:
      cur = self.table[h]
      while cur.next is not None and cur.key != key:
        cur = cur.next
      if cur.key == key:
        cur.val = val
      else:
        cur.next = LinkedListNode(key, val)

  def get(self, key):
    """
    Gets a value stored at the specified key,
    if the key is not in the table, it will
    return None

    """
    h = self.dot_product_hash(key)
    if self.table[h] is None:
      return None
    cur = self.table[h]
    while cur.next is not None and cur.key != key:
      cur = cur.next
    if cur.key == key:
      return cur.val
    return None
