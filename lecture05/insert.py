"""
B-Tree: Insertion
-----------------
A B-tree class which only implements insertion

"""


from search import BTreeSearchNode


class BTreeInsertNode(BTreeSearchNode):
  """
  Inherits from BTreeSearchNode in search.py

  """
  def __init__(self, t):
    BTreeSearchNode.__init__(self, t)

  def _create_new(self):
    """
    Instantiate a new B-tree node. This function
    will need to be overwritten when the node with
    deletion inherits from this class

    """
    return BTreeInsertNode(self.t)

  def _insert_non_full(self, key):
    """
    This is an auxilary function for the .insert()
    method above. It inserts a key into a node with
    less than (2 * t) - 1 keys

    """
    i = self.n - 1
    while i >= 0 and self.keys[i] > key:
        i -= 1
    if self.is_leaf():
      # if it's a leaf node, insert the new key into the keys list
      self.keys = self.keys[:i + 1] + [key] + self.keys[i + 1:]
    else:
      # Otherwise insert it into the proper child
      child = self.children[i + 1]
      if child.n == self.max_capacity:
        self._split_child(child, i + 1)
      if i != self.n - 1 and self.keys[i + 1] < key:
        i += 1
      self.children[i + 1]._insert_non_full(key)

  def _split_child(self, child, i):
    """
    Split one of the node's children into two,
    each with (t - 1) and t children

    This function modifies the node's key and children,
    it inserts the key at index i in self.keys
    and the new child at index i + 1 in self.children

    It also reduces the number of keys in self.children[i] to
    t - 1 and the number of children to t

    """
    new_node = self._create_new()

    for _ in range(self.t - 1):
      new_node.keys.append(child.keys.pop())
    new_node.keys.reverse()

    if not child.is_leaf():
      for _ in range(self.t):
        new_node.children.append(child.children.pop())
    new_node.children.reverse()

    self.children = \
        self.children[:i + 1] + [new_node] + self.children[i + 1:]

    self.keys = self.keys[:i] + [child.keys.pop()] + self.keys[i:]

  def insert(self, key):
    """
    Insert a node into the tree, assuming the current node
    is the current root. Returns the new root of the tree

    """
    if self.n == 0:
      self.keys.append(key)
      return self
    if self.n == self.max_capacity:
      new_root = self._create_new()
      new_root.children.append(self)
      new_root._split_child(self, 0)
      i = 0
      if new_root.keys[0] < key:
        i += 1
      new_root.children[i]._insert_non_full(key)
      return new_root
    self._insert_non_full(key)
    return self
