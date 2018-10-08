"""
AVL Tree Implementation
-----------------------
An AVL tree implementation
with parent pointers and where
each node stores the size of
its subtree

"""


class AVLTreeNode(object):
  """
  AVL Tree Node with size
  and parent pointers

  """
  def __init__(self, val):
    self.size = 1
    self.val = val
    self.left = self.right = self.parent = None

  def _decrease_parent_count(self):
    """
    Traverse the tree by parent pointer
    and update the size

    """
    if self.parent is not None:
      self.parent.size -= 1
      self.parent.decrease_parent_count()

  def _create_new(self, val):
    """
    Create a new tree node

    """
    return AVLTreeNode(val)

  def _insert(self, val):
    """
    Binary search tree insert function
    with size augmentation

    Complexity: O(log(N)) where N is number of nodes in the tree

    """
    if val == self.val:
      return self
    self.size += 1
    if val < self.val:
      if self.left is None:
        self.left = self._create_new(val)
        self.left.parent = self
        return self
      self.left = self.left._insert(val)
    else:
      if self.right is None:
        self.right = self._create_new(val)
        self.right.parent = self
        return self
      self.right = self.right._insert(val)
    return self

  def _delete(self, val):
    """
    Delete a value from a BST

    Complexity: O(log(N)) where N is number of nodes in the tree

    """
    if val == self.val:
      self._decrease_parent_count()
      if self.size == 1:  # leaf case
        return None
      if self.left is None:  # no left child case
        if self.parent is None:
          self.right.parent = None
          return self.right  # root case: right child is new root
        self.right.parent = self.parent
        return self.right
      if self.right is None:  # no right child case
        if self.parent is None:
          self.left.parent = None
          return self.left  # root case: left child is new root
        self.left.parent = self.parent
        return self.left
      # two children case: swap the value of this node with its successor then
      # recursively call delete on the right subtree
      tmp = self.right
      while tmp.left:
        tmp = tmp.left
      self.val, tmp.val = tmp.val, self.val
      if tmp == self.right:
        self.right = tmp._delete(val)
      else:
        tmp.parent.left = tmp._delete(val)
      return self
    if val < self.val and self.left is not None:
      self.left = self.left._delete(val)
    elif val > self.val and self.right is not None:
      self.right = self.right._delete(val)
    return self

  def _rotate_left(self):
    """
    Rotate a tree left and return the new root

    Modifies the size of the nodes as well

    """
    tmp = self.right
    tmp.parent = self.parent
    self.right = tmp.left
    if self.right is not None:
      self.right.parent = self
    tmp.left = self
    self.parent = tmp
    self.size -= 1 + (0 if tmp.right is None else tmp.right.size)
    tmp.size += 1 + (0 if self.left is None else self.left.size)
    return tmp

  def _rotate_right(self):
    """
    Rotate a tree right and return the new root

    Modifies the size of the nodes as well

    Same as rotate left but with any 'left' or 'right' keys
    switched

    """
    tmp = self.left
    tmp.parent = self.parent
    self.left = tmp.right
    if self.left is not None:
      self.left.parent = self
    tmp.right = self
    self.parent = tmp
    self.size -= 1 + (0 if tmp.left is None else tmp.left.size)
    tmp.size += 1 + (0 if self.right is None else self.right.size)
    return tmp

  def _get_left_height(self):
    """
    Get the height of the node's left subtree

    """
    if self.left is None:
      return 0
    return 1 + \
      self.left._get_left_height() + \
      self.left._get_right_height()

  def _get_right_height(self):
    """
    Get the height of the node's right subtree

    """
    if self.right is None:
      return 0
    return 1 + \
      self.right._get_left_height() + \
      self.right._get_right_height()

  def _balance(self):
    """
    Balances an AVL tree recursively

    """
    if self.left is not None:
      self.left = self.left._balance()
    if self.right is not None:
      self.right = self.right._balance()
    left_height = self._get_left_height()
    right_height = self._get_right_height()
    if abs(left_height - right_height) > 1:
      if left_height > right_height:
        return self._rotate_right()
      return self._rotate_left()
    return self

  def insert(self, val):
    """
    Insert a val into the subtree rooted at this node

    """
    node = self._insert(val)
    return node._balance()

  def delete(self, val):
    """
    Delete a val from the subtree rooted at this node

    """
    node = self._delete(val)
    return node._balance()


class Tree(object):
  """
  General balanced binary tree class
  which can use different types of nodes

  """
  def __init__(self, Node):
    self.Node = Node
    self.root = None

  def insert(self, val):
    if self.root is None:
      self.root = self.Node(val)
      return
    self.root = self.root.insert(val)

  def delete(self, val):
    if self.root is None:
      return
    self.root = self.root.delete(val)


class AVLTree(Tree):
  """
  AVL Tree

  """
  def __init__(self):
    Tree.__init__(self, AVLTreeNode)
