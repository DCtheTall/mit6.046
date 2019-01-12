"""
Lecture 15: Linear Programming
------------------------------
Linear programming is a method of optimization,
in this case minimization, of a set of parameters.

The goal is to find a vector

x in R^n

where given a vector

c in R^n

you want to minimize the scalar
product of x and c, given by

inner_product(x, c)
= dot(x, c)
= sum([x[i] * c[i] for i in range(n)])

given that x must follow a set of linear constraints
given by A_ub, A_eq, such that

A_ub * x <= b_ub

and

A_eq * x == b_eq

where

b_ub, b_eq in R^n.

The most used method is simplex which is exponential time in worst case
but in practice generally works well.

This program uses a simplex algorithm provided by the scipy library,
you can find more info on scipy here:

https://www.scipy.org/

The program implements the example on finding the optimal way
to distribute to win an election. The inputs, c, A_ub, b_ub,
are provided from the lecture.

"""


from scipy.optimize import linprog
from flownetwork import FlowNetwork
from graph import Graph


def political_advertising_example():
  """
  Below is a basic implementation of scipy.optimize's linprog
  function being used to solve the example in lecture.

  Since the lecture gave the constraints as lower bounds
  and scipy uses upper bounds, I had to negate the
  constraining inequalities.

  The problem is to find the minimum amount of money
  you need to spend in order to win an election, given
  how much you support one issue sways different
  demographics of the population.

  The objective function is: c = (1, 1, 1, 1)

 A_ub is a matrix of how funding a particular
 issue sways demographics and b_ub = how many
 votes of each demographic is needed to win a
 majority.

  """
  c = (1, 1, 1, 1)
  A_ub = \
      ((2, -8, 0, -10),
       (-5, -2, 0, 0),
       (-3, 5, -10, -2))
  b_ub = (-500000, -100000, -25000)
  return linprog(
    c, A_ub, b_ub, method='interior-point')


def maximum_flow_example():
  """
  Use linear programming to find the maximum flow
  through a flow network, G(V, E), a mathematical structure
  defined in lectures 13-14.

  The objective function c is a vector where each component
  is either 1 if there is an edge from the src to that vertex
  (vertices in sorted order) and 0 otherwise.

  The fact that

  c(u, v) >= f(u, v) forall (u, v) in E

  gives us the upper bound constraints. The equality
  constraints come from

  f(u, v) = -f(v, u)

  and

  sum(f(u, v)) = 0 where u, v in V - {src, sink}.

  scipy's linprog is able to get the correct answer
  we get using Ford-Fulkerson (ignoring floating point error).

  This example returns the negative of the max flow since
  linprog tries to find minimums. Multiplying the result by
  -1 will reveal the actual max flow.

  """
  network = FlowNetwork('s', 't', {
    ('s', 'a'): 3,
    ('s', 'b'): 2,
    ('a', 'd'): 2,
    ('b', 'a'): 3,
    ('b', 'c'): 3,
    ('c', 'd'): 3,
    ('c', 't'): 2,
    ('d', 'b'): 1,
    ('d', 't'): 3,
  })
  c = {
    v: -1 for u, v in network.flows
    if u == network.src
  }
  for u in network.vertices:
    if u not in c:
      c[u] = 0
  V_sorted = sorted(network.vertices)
  n = len(V_sorted)
  c = list(map(lambda u: c[u], V_sorted))
  A_ub = [[0] * n for _ in range(n)]
  A_eq = [[0] * n for _ in range(n)]
  for i, u in enumerate(V_sorted):
    for j, v in enumerate(V_sorted):
      if (u, v) in network.residual_capacities:
        A_ub[i][j] = 1
        if {u, v}.intersection(
          {network.src, network.sink}):
            continue
        A_eq[i][j] = 1
        A_eq[j][i] = -1
  b_ub = [
    sum([
      network.residual_capacities[(v, w)] if v == u else 0
      for v, w in network.residual_capacities
    ])
    for u in V_sorted
  ]
  b_eq = [0] * n
  return linprog(
    c, A_ub, b_ub, A_eq, b_eq, method='interior-point')


def shortest_path_example():
  """
  Single-source shortest path example

  This function is an implementation of using
  linear programming to solve the single source
  shortest path problem for a directed graph
  G(V, E) with non-negative edge weights given
  in the example here:

  https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/

  An example where you can verify the result of the
  linear program and compare it to the result from
  running Djikstra's on the same graph. The graph in
  this example is undirected, but the directions can
  be guessed so that the result is the same as Djikstra's.

  In this case the objective function is

  max(sum(d[u] for u in V))

  where d[u] is the minimum cost to get to the vertex u
  from the source vertex.

  The upper bound constrains are given by the triangle
  inequality, i.e.

  d[v] - d[u] <= w(u, v) for u, v in E

  and is given by the matrix A_ub and the vector b_ub.

  The equality constraint comes from the fact that

  sum([d[s] for e in E]) = 0,

  i.e. the shortest path from the source to itself
  is always 0.

  """
  graph = Graph({
    (0, 1): 4,
    (0, 7): 8,
    (1, 2): 8,
    (1, 7): 11,
    (2, 3): 7,
    (2, 5): 4,
    (2, 8): 2,
    (3, 4): 9,
    (3, 5): 14,
    (5, 4): 10,
    (6, 5): 2,
    (7, 6): 1,
    (6, 8): 6,
    (7, 8): 7,
  })
  src = 0
  V_sorted = sorted(graph.vertices)
  E_sorted = sorted(graph.edge_weights.keys())
  v = len(V_sorted)
  e = len(E_sorted)
  c = [-1] * v
  c[0] = 0
  A_ub = [
    [
      {u: -1, v: 1}[w] if w in (u, v) else 0
      for w in V_sorted
    ]
    for u, v in E_sorted
  ]
  b_ub = [
    graph.edge_weights[(u, v)]
    for u, v in E_sorted
  ]
  A_eq = [
    [
      1 if w == src else 0
      for w in V_sorted
    ]
    for u, v in E_sorted
  ]
  b_eq = [0] * e
  return linprog(
      c, A_ub, b_ub, A_eq, b_eq, method='interior-point')


if __name__ == '__main__':
  # print political_advertising_example()
  # print maximum_flow_example()
  # print shortest_path_example()
  pass
