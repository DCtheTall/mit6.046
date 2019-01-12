"""
Lecture 9: Augmentation
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
  def __init__(self, key):
    self.size = 1
    self.key = key
    self.min = key
    self.max = key
    self.left = self.right = self.parent = None

  def _decrease_parent_count(self):
    """
    Traverse the tree by parent pointer
    and update the size

    """
    if self.parent is not None:
      self.parent.size -= 1
      self.parent._decrease_parent_count()

  def _create_new(self, key):
    """
    Create a new tree node

    """
    return AVLTreeNode(key)

  def _insert(self, key):
    """
    Binary search tree insert function
    with size augmentation

    Complexity: O(log(N)) where N is number of nodes in the tree

    """
    if self.min > key:
      self.min = key
    if self.max < key:
      self.max = key
    if key == self.key:
      return self
    self.size += 1
    if key < self.key:
      if self.left is None:
        self.left = self._create_new(key)
        self.left.parent = self
        return self
      self.left = self.left._insert(key)
    else:
      if self.right is None:
        self.right = self._create_new(key)
        self.right.parent = self
        return self
      self.right = self.right._insert(key)
    return self

  def _update_min(self):
    """
    Update the minimum value when the current
    min value in the subtree is being deleted

    """
    tmp = self
    while tmp.left is not None:
      tmp = tmp.left
    return tmp.parent.key

  def _update_max(self):
    """
    Update the maximum value when the current
    max value in the subtree is being deleted

    """
    tmp = self
    while tmp.right is not None:
      tmp = tmp.right
    return tmp.parent.key

  def _get_successor(self):
    """
    Get this node's successor

    """
    tmp = self.right
    while tmp.left:
      tmp = tmp.left
    return tmp

  def _delete(self, key):
    """
    Delete a keyue from a BST

    Complexity: O(log(N)) where N is number of nodes in the tree

    """
    if key == self.key:
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

      # two children case: swap the keyue of this node with its successor then
      # recursively call delete on the right subtree
      tmp = self._get_successor()
      self.key, tmp.key = tmp.key, self.key
      if tmp == self.right:
        self.right = tmp._delete(key)
      else:
        tmp.parent.left = tmp._delete(key)
      return self

    if key == self.min:
      self._update_min()
    if key == self.max:
      self._update_max()

    if key < self.key and self.left is not None:
      self.left = self.left._delete(key)
    elif key > self.key and self.right is not None:
      self.right = self.right._delete(key)
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
    return 1 + max(
      self.left._get_left_height(),
      self.left._get_right_height(),
    )

  def _get_right_height(self):
    """
    Get the height of the node's right subtree

    """
    if self.right is None:
      return 0
    return 1 + max(
      self.right._get_left_height(),
      self.right._get_right_height(),
    )

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

  def search(self, key):
    """
    Search the binary tree for a node containing
    the provided keyue

    """
    if self.key == key:
      return self
    if self.key > key:
      return None if self.left is None else self.left.search(key)
    return None if self.right is None else self.right.search(key)


  def insert(self, key):
    """
    Insert a key into the subtree rooted at this node

    """
    node = self._insert(key)
    return node._balance()

  def delete(self, key):
    """
    Delete a key from the subtree rooted at this node

    """
    node = self._delete(key)
    return node._balance()

  def traverse(self):
    """
    Return all keys inorder
    in the subtree rooted at the current node

    """
    if self.key < self.min or self.key > self.max:
      raise KeyError(
          'AVLTreeNode has a key out of range')
    res = ''
    if self.left is not None:
      res += self.left.traverse()
    res += str(self.key) + ' '
    if self.right is not None:
      res += self.right.traverse()
    return res


class BinaryTree(object):
  """
  General balanced binary tree class
  which can use different types of nodes

  """
  def __init__(self, Node):
    self.Node = Node
    self.root = None

  def search(self, key):
    """
    Search the tree for the node
    containing the provided keyue

    """
    if self.root is None:
      return None
    return self.root.search(key)

  def insert(self, key):
    """
    Insert a keyue into the tree

    """
    if self.root is None:
      self.root = self.Node(key)
    else:
      self.root = self.root.insert(key)

  def delete(self, key):
    """
    Delete a keyue in the tree

    """
    if self.root is None:
      raise KeyError(
        'Cannot delete keyue {} from an empty tree'.format(key))
    self.root = self.root.delete(key)

  def traverse(self):
    """
    Traverse the tree and return all keys as strings

    """
    if self.root is None:
      return ''
    return self.root.traverse()


class AVLTree(BinaryTree):
  """
  AVL Tree

  """
  def __init__(self):
    BinaryTree.__init__(self, AVLTreeNode)
