"""
All-Pairs Shortest Paths
------------------------
Matrix multiplication method

"""


from graph import Graph


def multiply_adjacency_matrices(vertices, A, B):
  """
  'Multiply' two adjacency matrices where multiplication
  and addition are defined as:

  multiply: add values together
  add: take the minimum value

  These operations with matrices form a semiring
  https://en.wikipedia.org/wiki/Semiring

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
  squares method, you only do O(log(v)) multiplications.

  This method beats the one in dp.py but is slower than the
  Floyd-Warshall algorithm

  """
  if not isinstance(graph, Graph):
    raise TypeError(
      'matrix_multiply_all_pairs_shortest_paths must be called with an instance of Graph')
  i = 0
  dp = {0: graph.edges}
  while (1 << i) <= (graph.v - 1):
    dp[i + 1] = multiply_adjacency_matrices(graph.vertices, dp[i], dp[i])
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
