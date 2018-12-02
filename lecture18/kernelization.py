"""
Lecture 18: Fixed-Parameter Algorithms
Kernelization
-------------
For fixed-parameter tractible problems, kernelization
is a polynomial-time algorithm which takes an input
to an FPT algorithm and a parameter, (X, k), and
transforms it into a smaller input (X', k') such that
the two inputs are equivalent (i.e. the output of the
decision problem is the same for (X, k) and (X', k')).

This program contains a kernelization algorithm for
the k-Vertex Cover problem which reduces the runtime
of the brute force and bounded search tree methods.

"""


from kvertexcover import (
  Graph,
  brute_force_k_vertex_cover,
  bounded_search_tree_k_vertex_cover,
)


def k_vertex_cover_kernelize(graph, k):
  """
  This function is a kernelization algorithm
  for the Graph class defined in kvertexcover.py
  for the k-Vertex Cover problem.

  The kernelization algorithm reduces the size
  of the graph being considered and can reduce
  the runtime of both the brute force and
  bounded search tree algorithms.

  If any vertex, u, has a degree greater than k, then u must be in the vertex
  cover, S, such that |S| <= k because any other vertex cover must have
  more than k vertices to cover each edge incident on u. So delete u from the
  graph and its incident edges then decrement k.

  This implementation skips a step covered in lecture, removing any loops
  or multi-edges from the graph, making it a simple gtaph. This is omitted
  because in kvertexcover.py we assumed the graph is simple (i.e. it has no
  loops and no multi-edges).

  After the kernelization process, each vertex left must have
  a degree <= k. So if a vertex cover, S, exists such that |S| <= k,
  then this implies that there can only be at most k^2 edges and
  2 * (k^2) vertices in the worst case. This means that after
  kernelization if |V| + |E| > 3 * k^2 then there is no vertex
  cover, S, such that |S| <= k.

  Also if a solution exists then after kernelization, then

  O(V + E) = O(k^2)

  Time complexity: O(V * E)

  """
  kernelized_graph = graph.copy()
  k_prime = k
  for u in graph.vertices:
    if len(graph.adjacency_list[u]) > k:
      kernelized_graph.delete_vertex_and_incident_edges(u)
      k_prime -= 1
      if k_prime == 0:
        break
  return (kernelized_graph, k_prime)


def kernelized_brute_force_k_vertex_cover(graph, k):
  """
  Kernelized brute force k-Vertex Cover.

  Time complexity: O((V * E) + (2^k * k^(2k + 2)))

  """
  if not isinstance(graph, Graph):
    raise TypeError(
      'the first argument of brute_force_k_vertex_cover must be an instance of Graph')
  if not isinstance(k, int) or k <= 0 or len(graph.vertices) < k:
    raise Exception(
      'k must be a a positive integer less than or equal to than the number of vertices in the graph')
  kernelized_graph, k_prime = k_vertex_cover_kernelize(graph, k)
  if k_prime == 0:
    return len(kernelized_graph.edges) == 0
  v, e = len(kernelized_graph.vertices), len(kernelized_graph.edges)
  if v > k * (k + 1) or e > k ** 2:
    return False
  return brute_force_k_vertex_cover(kernelized_graph, k_prime)


def kernelized_bounded_search_tree_k_vertex_cover(graph, k):
  """
  Kernelized bounded search tree k-Vertex Cover.

  Time complexity: O((V * E) + (2^k * k^2))

  """
  if not isinstance(graph, Graph):
    raise TypeError(
      'the first argument of brute_force_k_vertex_cover must be an instance of Graph')
  if not isinstance(k, int) or k < 0 or len(graph.vertices) < k:
    raise Exception(
      'k must be a a positive integer less than or equal to than the number of vertices in the graph')
  kernelized_graph, k_prime = k_vertex_cover_kernelize(graph, k)
  if k_prime == 0:
    return len(kernelized_graph.edges) == 0
  v, e = len(kernelized_graph.vertices), len(kernelized_graph.edges)
  if v > k * (k + 1) or e > k ** 2:
    return False
  return bounded_search_tree_k_vertex_cover(kernelized_graph, k_prime)
