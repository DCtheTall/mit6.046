"""
Lecture 11: All-Pairs Shortest Paths
Matrix Multiplication Method
----------------------------
All pairs shortest path matrices multiplication
method.

"""


from graph import Graph


def multiply_adjacency_matrices(vertices, A, B):
  """
  'Multiply' two adjacency matrices where multiplication
  and addition are defined as:

  multiply: add values together
  add: take the minimum value

  Since normal multiplication for n x n matrices looks like:

  C[(i, j]] = sum([
    A[(i, k)] * B[(k, j)]
    for k in range(n)
  ])

  With our new definition of addition and multiplication,
  the operation becomes:

  C[(i, j)] = min([
    A[(i, k)] + B[(k, j)]
    for k in range(n)
  ])

  This new operation is the same as relaxing edges
  in the 1st DP approach.

  These operations with matrices form a semiring

  https://en.wikipedia.org/wiki/Semiring

  which is a mathematical structure like a ring but
  without the property of an additive inverse
  (min is not invertible).

  Complexity: O(v ** 3)

  """
  result = dict()
  for u in vertices:
    for v in vertices:
      result[(u, v)] = min([
        A[(u, x)] + B[(x, v)]
        for x in vertices
      ])
  return result


def matrix_multiply_all_pairs_shortest_paths(graph):
  """
  Matrix multiplication method for finding the lowest
  path weights between all vertices in the graph.

  Complexity: O((v ** 3) * log(v))

  Each matrix multiply is O(v ** 3) and by using the repeated
  squaring method you only perform O(log(v)) multiplications.

  This method beats the one in dp.py but is slower than the
  Floyd-Warshall algorithm

  """
  if not isinstance(graph, Graph):
    raise TypeError(
      'matrix_multiply_all_pairs_shortest_paths must be called with an instance of Graph')
  i = 0
  dp = {0: graph.edges}
  while (1 << i) <= (graph.v - 1):
    dp[i + 1] = \
      multiply_adjacency_matrices(
        graph.vertices, dp[i], dp[i])
    i += 1
  result = {(u, v): 0 for u, v in graph.edges}
  while i >= 0:
    if (1 << i) & (graph.v - 1) != 0:
      for u, v in result:
        result[(u, v)] += dp[i][(u, v)]
    i -= 1
  for u in graph.vertices:
    for v in graph.vertices:
      for x in graph.vertices:
        if result[(u, v)] > result[(u, x)] + result[(x, v)]:
          raise Exception('Negative weight cycle')
  return result
