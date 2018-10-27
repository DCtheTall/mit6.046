"""
Disjoint-Set
------------

A disjoint-set is a data structure which supports the
following operations:

- MakeSet(u) make set for a key if it is not in the disjoint-set, O(1) time
- FindSet(u) find the key u in the disjoint set in approx O(1)
- Union(u, v) merge the sets containing u and v
              if they are not already in the same set
              also O(1) time

"""


class TreeNode(object):
  """
  TreeNode is a node in the underlying tree data structure
  in the disjoint-set

  """
  def __init__(self, key):
    self.key = key
    self.parent = self
    self.size = 1


class DisjointSet(object):
  """
  DisjointSet contains a hashmap to
  each tree node by key. This allows us to find
  a node in O(1)

  """
  def __init__(self):
    self.trees = dict()

  def make_set(self, u):
    """
    MakeSet creates a single TreeNode
    if the provided key is not already
    in the tree

    """
    if u not in self.trees:
      self.trees[u] = TreeNode(u)

  def find_set(self, u):
    """
    FindSet searches for the tree containing the key
    and returns the root

    It also reassigns every trees parent pointer
    to its grandparent to speed up future searching

    """
    cur = self.trees[u]
    while cur.parent != cur:
      cur, cur.parent = cur.parent, cur.parent.parent
    return cur

  def union(self, u, v):
    """
    Union by size always has the smaller tree become a child
    of the root of the larger tree

    """
    u_root = self.find_set(u)
    v_root = self.find_set(v)
    if u_root == v_root:
      return
    u_root, v_root = \
      u_root if u_root.size > v_root else v_root, \
      v_root if u_root.size > v_root else u_root
    v_root.parent = u_root
    u_root.size += v_root.size
