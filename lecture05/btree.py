"""
Lecture 5: Amortization
B-Tree Python implementation
----------------------------
The lecture mentions 2-3 trees which
are a specific form of a more general
data structure called a B-tree.
A 2-3 tree is a BTree with a minimum degree (t) of 2.

Minimum degree (t):
-------------------

Any non-leaf node that is not the root must have
at least t children

Any node can only have
up to (2 * t) - 1 children

These are the rules that keep the B-tree self-balancing.

Below is a example of the general B-tree
data structure. The definitions are separated by
primary function into modules for organization.

Searching the tree: search.py
Inserting into the tree: insert.py
Deleting from the tree: delete.py

Each class inherits from the previous module, w the obvious
exception of the first one

This implementation is based on the example here:
https://www.geeksforgeeks.org/b-tree-set-1-introduction-2/

"""


from remove import BTreeDeleteNode as BTreeNode


class BTree(object):
  """
  B-tree class using the nodes defined
  in the other programs

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
      self.root = BTreeNode(self.t)
    self.root = self.root.insert(key)

  def remove(self, key):
    if self.root is None:
      raise KeyError(
        'key {} is not in B-tree'.format(key))
    self.root = self.root.remove(key)
    if self.root.n == 0:
      self.root = self.root.children[0]

  def traverse(self):
    """
    Traverse the tree and return the values inorder

    """
    if self.root is None:
      return ''
    return self.root.traverse()
