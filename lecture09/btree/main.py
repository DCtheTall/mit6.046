"""
Augmented B-Tree: Insertion
---------------------------
This folder contains an implementation of an augmented B-tree.
For this implementation, the tree only stores data in its leaf
nodes. Each node also has level-set pointers defined here which
access the left and right siblings of each node (or None if they do not exist).
Each node also has a min/max key which store the minimum and maximum values
stored in the node or its children if it's not a leaf.

This implementation is optimized for finger-searching, i.e. finding a particular
value starting at a given node

"""


from insert import BTreeInsertNode as Node


class FingerSearchBTree(object):
  """
  B-tree class using the augmented nodes
  that satisfy the finger-search property

  """

  def __init__(self, t):
    self.root = None
    self.t = t

  def search(self, key):
    """
    Search the B-tree for the node
    containing a provided key

    """
    if self.root is None:
      return None
    return self.root.search(key)

  def insert(self, key):
    """
    Insert a provided key into the tree

    """
    if self.root is None:
      self.root = Node(self.t)
    self.root = self.root.insert(key)

  def remove(self, key):
    if self.root is None:
      raise KeyError(
          'key {} is not in B-tree'.format(key))
    self.root = self.root.remove(key)

  def traverse(self):
    """
    Traverse the tree and return the values inorder

    """
    if self.root is None:
      return ''
    return self.root.traverse()
