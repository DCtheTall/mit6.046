"""
Lecture 23:
Cache Oblivious Algorithms
--------------------------
This lecture is the first that covers cache-oblivious algorithms,
a class of algorithms that use a computer's cache in a memory
heirarchy system efficiently. These algorithms perform well on
machines with different cache sizes or a memory hierarchy on a
single machine.

The first algorithm covered in lecture is a linear scan. In this
example, we sum an array of size N using a block size B with memory
accesses on the order of O((N / B) + 1). This is achieved by storing
the array contiguously in memory, which amortizes the cost of accessing
successive elements in the array.

Below is an object oriented model of the process using abstract data
types. For this example each word is an integer, stored in

"""


from collections import deque
from uuid import uuid1


class Store(object):
  """
  Store object represents a memory store
  of blocks somewhere in a computer's
  memory. It stores the total number of
  words it can store, M, and the block
  size, B. It has a FIFO queue for when
  the cache is full, which it uses to write
  data to its parent in the memory heirarchy.

  """
  def __init__(self, M, B, parent=None):
    self.M = M
    self.B = B
    self.memory = dict()
    self.q = deque()
    self.parent = parent

  def delete(self, key):
    """
    Delete the data stored at the provided address
    from the store's memory.

    """
    del self.memory[key]
    q = list(self.q)
    q.pop(q.index(key))
    self.q = deque(q)

  def get(self, key):
    """
    Get the data stored at a particular address,
    key, if the key is not found in the store,
    the store retrieves the data from its parent
    in the memory heirarchy and caches it.

    """
    if key in self.memory:
      return self.memory[key]
    data = self.parent.get(key)
    self.parent.delete(key)
    self.set(key, data)
    return data

  def set(self, key, data):
    """
    Store the data in the provided address
    in the store. If the cache is full, it
    deqeues the FIFO array of addresses in
    the cache and deletes the first one
    that was added.

    """
    if self.B * len(self.memory) == self.M:
      k = self.q.popleft()
      self.parent.set(k, self.memory[k])
      del self.memory[k]
    self.memory[key] = data
    self.q.append(key)


class ContiguousArray(object):
  """
  ContiguousArray is an array of integers
  which writes contiguous blocks of memory.
  It can hold one block of data in working
  memory, and if it needs to access a block
  that is not in working memory, it reads a
  new block from the memory cache and overwrites
  it.

  This data structure is able to sum its elements
  in O((N / B) + 1) operations because it stores
  its elements contriguously, which amortizes the
  cost of reading blocks from memory for subsequent
  reads from the array.

  You can do a linear scan from the memory
  model to sum the array using the Python sum
  function.

  """
  def __init__(self, store):
    self.length = 0
    self.cur_block_index = None
    self.cur_block = None
    self.addresses = dict()
    self.store = store

  def __iter__(self):
    """
    Iterator for the array.

    """
    return (self[i] for i in range(self.length))

  def __len__(self):
    """
    Return the length of the array.

    """
    return self.length

  def __getitem__(self, index):
    """
    Get the value at an index of the array
    using the subscript operator.

    """
    if index < 0 or index >= self.length:
      raise IndexError('Index out of range')
    base_index = (index // self.store.B) * self.store.B
    if self.cur_block is None or self.cur_block_index != base_index:
      self.cur_block_index = base_index
      self.cur_block = self.store.get(self.addresses[base_index])
    return self.cur_block[index - base_index]

  def append(self, block):
    """
    Append a full block of integers to
    the array and store them in the cache.

    """
    if len(block) != self.store.B:
      raise Exception('Invalid block size')
    key = uuid1()
    self.addresses[self.length] = key
    self.store.set(key, block)
    self.length += self.store.B
