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
    if self.parent is None:
      return None
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
  It uses an instance of the Store for the
  main memory for the process using the
  array, and its parent can be another Store
  instance representing the machine's cache.

  This data structure is able to sum its elements
  in O((N / B) + 1) memory transfers because it stores
  its elements contriguously, which amortizes the
  cost of transferring blocks from memory for subsequent
  reads from the array.

  You can do a linear scan from the memory
  model to sum the array using the Python sum
  function.

  """
  def __init__(self, store = Store(1024, 64, Store(float('inf'), 64))):
    self.length = 0
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
    block = self.store.get(self.addresses[base_index])
    return block[index - base_index]

  def __setitem__(self, index, value):
    """
    Set an index in the array, this can be used for parallel scans.

    """
    self[index] # pull correct block into working memory
    base_index = (index // self.store.B) * self.store.B
    block = self.store.get(self.addresses[base_index])
    block[index - base_index] = value

  def append(self, val):
    """
    Append a value to the array.

    """
    base_index = (self.length // self.store.B) * self.store.B
    block = None
    if base_index in self.addresses:
      block = self.store.get(self.addresses[base_index])
    if block is None:
      key = int(uuid1())
      self.addresses[self.length] = key
      block = [None] * 8
      block[0] = val
      self.store.set(key, block)
    else:
      block[self.length - base_index] = val
    self.length += 1
