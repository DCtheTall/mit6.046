"""
Lecture 10: Dynamic Programming
Optimal BST structure
---------------------
Let's say we have a set of n keys to insert into a binary
search tree and each key, k_0, k_1, ..., k_i, ..., k_(n - 1) has an associated
search probability w_i.

We want to construct the "optimal" binary search tree where
the cost function:

e(T) = sum([
  depth(k_i in T) * w_i
  for i in range(n)
])

where T is the tree.

"""


class BSTNode(object):
  """
  The binary tree node used for constructing
  the tree. It has the standard insert() and search()
  defined. It also has an additional method

  """
  def __init__(self, key):
    self.key = key
    self.left = self.right = None

  def insert(self, key):
    if self.key == key:
      return
    if self.key > key and self.left is None:
      self.left = BSTNode(key)
      return
    if self.key > key:
      self.left.insert(key)
      return
    if self.right is None:
      self.right = BSTNode(key)
      return
    self.right.insert(key)

  def search(self, key):
    if self.key == key:
      return self
    if self.key > key and self.left is not None:
      return self.left.search(key)
    if self.key < key and self.right is not None:
      return self.right.search(key)
    return None

  def traverse(self):
    res = ''
    if self.left is not None:
      res += self.left.traverse()
    res += str(self.key) + ' '
    if self.right is not None:
      res += self.right.traverse()
    return res

  def cost(self, weights, depth):
    """
    Compute the cost of a binary search tree node
    using the cost function defined above

    """
    depth += 1
    res = depth * weights[self.key]
    if self.left is not None:
      res += self.left.cost(weights, depth)
    if self.right is not None:
      res += self.right.cost(weights, depth)
    return res


def greedy_optimal_bst(keys, weights):
  """
  Use a greedy algorithm to construct an
  optimal binary search tree for searching
  keys in a list of keys, each with a weight
  stored in the dictionary, weights.

  The greedy algorithm chooses the key in the
  list with the largest weight to be the root
  of the tree, then populates its children
  with each key less than or greater than the
  tree.

  This algorithm however fails for the following
  keys and weights sets

  keys = [1, 2, 3, 4]
  weights = {
    1: 1,
    2: 10,
    3: 8,
    4: 9,
  }

  The greedy algorithm produces the following tree:

     .2.
  .1.   .4.
      .3.

  e(T) = (1 * 10) + (2 * (1 + 9)) + (3 * 8) = 54

  Where the actual optimal BST is

       .3.
    .2.   .4.
  .1.

  e(T) = (1 * 8) + (2 * (10 + 9)) + (3 * 1) = 49

  """
  n = len(keys)
  if n == 0:
    return None
  if n == 1:
    return BSTNode(keys[0])
  k_min = max(keys, key=weights.get)
  i = keys.index(k_min)
  root = BSTNode(k_min)
  root.left = greedy_optimal_bst(keys[:i], weights)
  root.right = greedy_optimal_bst(keys[i + 1:], weights)
  return root


def sum_weights(keys, weights, i, j):
  """
  Sum all weights from index i to j

  """
  return sum([
    weights[keys[k]]
    for k in range(i, j + 1)])


def dp_optimal_bst_weight(dp, keys, weights, i, j):
  """
  Get the optimal cost for a set of keys and associated
  weights for a BST

  This recursion is covered in the lecture

  """
  if i > j:
    return 0
  if i == j:
    return weights[keys[i]]
  if (i, j) in dp:
    return dp[(i, j)]
  if i + 1 == j:
    return min(
      weights[keys[i]] + (2 * weights[keys[j]]),
      weights[keys[j]] + (2 * weights[keys[i]]),
    )
  dp[(i, j)] = min([
    dp_optimal_bst_weight(dp, keys, weights, i, r - 1) + \
      dp_optimal_bst_weight(dp, keys, weights, r + 1, j) + \
      sum_weights(keys, weights, i, j)
    for r in range(i, j + 1)
  ])
  return dp[(i, j)]


def optimal_bst_weight(keys, weights):
  """
  Get the optimal BST given the provided keys
  and associated weights

  """
  return dp_optimal_bst_weight(
    dict(), keys, weights, 0, len(keys) - 1)


def get_weight_and_tree(func, dp, keys, weights, i, j, r):
  """
  Get the BST created at this particular value of r
  given a range i and j

  The first argment is the recursive function
  defined below for finding the optimal BST
  given the cost function above

  """
  node = BSTNode(keys[r])
  w_l, node.left = func(dp, keys, weights, i, r - 1)
  w_r, node.right = func(dp, keys, weights, r + 1, j)
  return (
    sum_weights(keys, weights, i, j) + w_l + w_r,
    node,
  )


def dp_optimal_bst(dp, keys, weights, i, j):
  """
  Recursive function to get the optimal BST
  given the cost function defined above

  It returns a tuple with the lowest possible
  cost and the best BST

  It uses memoization to speed up performance
  with a Python dictionary named dp "dynamic programming"

  """
  if (i, j) in dp:
    return dp[(i, j)]
  if i > j:
    dp[(i, j)] = (0, None)
  elif i == j:
    dp[(i, j)] = (weights[keys[i]], BSTNode(keys[i]))
  elif i + 1 == j:
    node_i = BSTNode(keys[i])
    node_i.right = BSTNode(keys[j])
    node_j = BSTNode(keys[j])
    node_j.left = BSTNode(keys[i])
    dp[(i, j)] = min(
      [
        (weights[keys[i]] + (2 * weights[keys[j]]), node_i),
        (weights[keys[j]] + (2 * weights[keys[i]]), node_j),
      ],
      key=lambda d: d[0],
    )
  else:
    dp[(i, j)] = min(
      [
        get_weight_and_tree(
          dp_optimal_bst, dp, keys, weights, i, j, r)
        for r in range(i, j + 1)
      ],
      key=lambda d: d[0],
    )
  return dp[(i, j)]


def optimal_bst(keys, weights):
  """
  Get the optimal BST using the cost function
  above given a list of keys and their associated weights

  """
  return dp_optimal_bst(
    dict(), keys, weights, 0, len(keys) - 1)
