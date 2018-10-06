"""
AVL Tree Implementation
-----------------------
An AVL tree implementation
with parent pointers and where
each node stores the size of
its subtree

"""


class TreeNode(object):
  """
  AVL Tree Node with size
  and parent pointers

  """
  def __init__(self, val):
    self.size = 1
    self.val = val
    self.left = self.right = self.parent = None

  def decrease_parent_count(self):
    """
    Traverse the tree by parent pointer
    and update the size

    """
    if self.parent is not None:
      self.parent.size -= 1
      self.parent.decrease_parent_count()


def bst_insert(node, val):
  """
  Binary search tree insert function
  with size augmentation

  Complexity: O(log(N)) where N is number of nodes in the tree

  """
  if val == node.val:
    return node
  node.size += 1
  if val < node.val:
    if node.left is None:
      node.left = TreeNode(val)
      node.left.parent = node
      return node
    node.left = bst_insert(node.left, val)
  else:
    if node.right is None:
      node.right = TreeNode(val)
      node.right.parent = node
      return node
    node.right = bst_insert(node.right, val)
  return node


def bst_delete(node, val):
  """
  Delete a value from a BST

  Complexity: O(log(N)) where N is number of nodes in the tree

  """
  if val == node.val:
    node.decrease_parent_count()
    if node.size == 1: # leaf case
      if node.parent is None:
        return None # root case
      return None
    if node.left is None: # no left child case
      if node.parent is None:
        node.right.parent = None
        return node.right # root case: right child is new root
      node.right.parent = node.parent
      return node.right
    if node.right is None: # no right child case
      if node.parent is None:
        node.left.parent = None
        return node.left  # root case: left child is new root
      node.left.parent = node.parent
      return node.left
    # two children case: swap the value of this node with its successor then
    # recursively call delete on the right subtree
    tmp = node.right
    while tmp.left:
      tmp = tmp.left
    node.val, tmp.val = tmp.val, node.val
    if tmp == node.right:
      node.right = bst_delete(tmp, val)
    else:
      tmp.parent.left = bst_delete(tmp, val)
    return node
  if val < node.val and node.left is not None:
    node.left = bst_delete(node.left, val)
  elif val > node.val and node.right is not None:
    node.right = bst_delete(node.right, val)
  return node


def tree_height(node):
  """
  Get the height of a TreeNode

  """
  if node is None:
    return 0
  return 1 + max(tree_height(node.left), tree_height(node.right))


def rotate_left(node):
  """
  Rotate a tree left and return the new root

  Modifies the size of the nodes as well

  """
  tmp = node.right
  tmp.parent = node.parent
  node.right = tmp.left
  if node.right is not None:
    node.right.parent = node
  tmp.left = node
  node.parent = tmp
  node.size -= 1 + (0 if tmp.right is None else tmp.right.size)
  tmp.size += 1 + (0 if node.left is None else node.left.size)
  return tmp


def rotate_right(node):
  """
  Rotate a tree right and return the new root

  Modifies the size of the nodes as well

  Same as rotate left but with any 'left' or 'right' keys
  switched

  """
  tmp = node.left
  tmp.parent = node.parent
  node.left = tmp.right
  if node.left is not None:
    node.left.parent = node
  tmp.right = node
  node.parent = tmp
  node.size -= 1 + (0 if tmp.left is None else tmp.left.size)
  tmp.size += 1 + (0 if node.right is None else node.right.size)
  return tmp



def avl_balance(node):
  """
  Balances an AVL tree recursively

  """
  if node is None:
    return None
  node.left = avl_balance(node.left)
  node.right = avl_balance(node.right)
  left_height = tree_height(node.left)
  right_height = tree_height(node.right)
  if abs(left_height - right_height) > 1:
    if left_height > right_height:
      return rotate_right(node)
    return rotate_left(node)
  return node


def avl_insert(node, val):
  """
  Insert a node into an AVL tree

  """
  return avl_balance(bst_insert(node, val))


def avl_delete(node, val):
  """
  Delete a node from an AVL tree

  """
  return avl_balance(bst_delete(node, val))


if __name__ == '__main__':
  tree = TreeNode(0)
  for i in range(1, 11):
    tree = avl_insert(tree, i)
  tree = avl_delete(tree, 0)
  print tree.val, tree.size
