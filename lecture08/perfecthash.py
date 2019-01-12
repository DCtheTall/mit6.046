"""
Lecture 8: Randomization
Minimal Perfect Hasing
----------------------
An implementation of the minimal perfect hash table
described in the article:

http://stevehanov.ca/blog/index.php?id=119

"""


import sys


DICTIONARY = '/usr/share/dict/words'


def load_dict():
  """
  Load the dictionary in the OS

  """
  D = dict()
  line = 0
  for key in open(DICTIONARY, 'r').readlines():
    D[key.strip()] = line
    line += 1
  return D


class PerfectHashTable(object):
  @staticmethod
  def hash(d, key):
    """
    Universal hash function using the FNV algorithm from this
    site:

    http://isthe.com/chongo/tech/comp/fnv/

    """
    if d == 0:
      d = 0x01000193
    for c in key:
      d = ((d * 0x01000193) ^ ord(c)) & 0xffffffff
    return d

  def __init__(self, D):
    """
    Create a perfect hash table using
    a given Python dictionary D

    G is the first hash table which contains a
    integers which are used to choose the hash function
    to find the key in the second table V which holds
    the value stored in the table

    """
    size = len(D)
    buckets = [[] for _ in range(size)]
    G = [0] * size
    V = [None] * size

    for key in D.keys():
      buckets[PerfectHashTable.hash(0, key) % size].append(key)
    buckets.sort(key=len, reverse=True)

    # Pick a hash function to store the base integer value, d, in the table
    # G, and the value that hash(d, value) in V
    for i, bucket in enumerate(buckets):
      if len(bucket) <= 1:
        break
      d = 1
      item = 0
      slots = []
      while item < len(bucket):
        slot = PerfectHashTable.hash(d, bucket[item]) % size
        if slot in slots or V[slot] is not None:
          d += 1
          item = 0
          slots = []
        else:
          item += 1
          slots.append(slot)
      G[PerfectHashTable.hash(0, bucket[0]) % size] = d
      for k, b in enumerate(bucket):
        V[slots[k]] = D[b]
      if (i % 1e3) == 0:
        print 'bucket {}  finished'.format(i)

    # After going through all the buckets with length > 1, insert
    # the remaining values into the remaining slots through trial and
    # error
    freelist = [k for k, value in enumerate(V) if value is None]
    for i in range(i, size):
      bucket = buckets[i]
      if len(bucket) == 0:
        break
      slot = freelist.pop()
      G[PerfectHashTable.hash(0, bucket[0]) % size] = -slot - 1
      V[slot] = D[bucket[0]]
      if (i % 1e3) == 0:
        print 'bucket {}  finished'.format(i)

    self.G = G
    self.V = V
    self.size = size

  def get(self, key):
    """
    Get the value stored at key

    """
    d = self.G[PerfectHashTable.hash(0, key) % self.size]
    if d < 0:
      return self.V[-d - 1]
    return self.V[PerfectHashTable.hash(d, key) % self.size]


if __name__ == '__main__':
  print 'Reading words from OS'
  D = load_dict()
  print 'Creating hash table'
  t = PerfectHashTable(D)
  for word in sys.argv[1:]:
    line = t.get(word)
    print '{} is on line {}'.format(word, line)



