"""
Simplex Algorithm
-----------------
The simplex algorithm is a linear programming (LP)
solver. See lingprog.py for a description of linear
programming.

In this case, given a vector

c in R^n

we are trying to find a vector

x in R^n where x[i] >= 0

which maximizes the dot product of x and c given
the constraints that

A * x <= b

where

b in R^m

and

A in R^(m x n)

i.e. in the set of all matrices with m rows and n columns.
The goal of simplex is to maximize the quantity

z = sum(c[i] * x[i] for i in range(n)).

In order to do so, we define the "basic" variables

x_b = [
  b_ub[j] - sum(A_ub[j][i] * x[i] for i in range(n))
  for j in range(m)
]

From the provided constraints, we see that each x[j] >= 0.

Let X_b be an m x m diagonal matrix where each element in the
diagonal is

X_b[i][i] = x_b[i].

This allows us to construct the initial tableau

| -c^T  0_m^T     1     0 |
| A_ub    X_b   0_m  b_ub |

where 0_m is the 0 vector in m dimensional space.
The resulting tableau is stored as a 2 dimensional
matrix using the SimplexTableau class.

"""


class SimplexTableau(object):
  """
  SimplexTableau class is an abstract type
  used to represent the simplex tableau
  for evaluating the simplex algorithm. For
  more information on this formulation of simplex,
  see:

  https://en.wikipedia.org/wiki/Simplex_algorithm
  http://www.math.wsu.edu/faculty/dzhang/201/Guideline%20to%20Simplex%20Method.pdf

  The constructor builds the initial tableau given
  the linear program.

  """
  def __init__(self, c, A_ub, b_ub):
    n, m = len(c), len(b_ub)
    cols = 2 + n + m
    rows = m + 1
    self.tableau = [
      [None for _ in range(cols)]
      for _ in range(rows)
    ]
    for i in range(rows):
      for j in range(cols):
        if i == 0:
          if j < n:
            self.tableau[0][j] = -c[j]
          elif j < n + m:
            self.tableau[0][j] = 0
          elif j == n + m:
            self.tableau[0][j] = 1
          elif j == (n + m) + 1:
            self.tableau[0][j] = 0
        else:
          if j < n:
            self.tableau[i][j] = A_ub[i - 1][j]
          elif j < n + m:
            self.tableau[i][j] = 1 if i - 1 == j - n else 0
          elif j == n + m:
            self.tableau[i][j] = 0
          else:
            self.tableau[i][j] = b_ub[i - 1]

  def get_objective_metric(self):
    """
    Get the current value of the objective function
    from the tableau's current state

    """
    return self.tableau[0][-1]

  def pivot_step(self):
    """
    Perform a "pivot" step of the simplex algorithm.

    The way to select a basic variable
    """
    pass
