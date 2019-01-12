"""
Lecture 15: Linear Programming
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

We then iterate over this data structure using a
pivot step until an optimal solution is found.

Each pivot step is executed in 4 distinct actions:

1. Pivot column selection:

Select the column (pivot_j) in those first n + m
columns which has the smallest negative element
in the first row.

The first n + m columns of the first row represent
the coefficients of each of the variables in the objective
function.

The selected column is the non-basic variable
with the most "leverage" on the objective function.

2. Pivot row selection:

Select the row pivot_i in the tableau matrix T such that

T[pivot_i][pivot_j] = min(
  T[i][-1] / T[i][pivot_j]
  for i in range(1, n + m)
)

This row represents the "tightest" constraint on the
selected column variable because

T[i][-1] / T[i][pivot_j]

is the maximum value of that variable it can be
if all others are set to 0 without violating the
constraint.

3. Row reduction:

Multiply each element in the selected pivot row by the
reciprocal of chosen pivot element, i.e.

T[pivot_i][pivot_j].

The pivot element is now 1.

4. Variable elimination:

For each row i except for the selected pivot row,
select the element in the pivot_j

el = T[i][pivot_j]

and add the pivot row times the additive
inverse of el. This way afterwards

T[i][pivot_j] = 0.

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
    self.m, self.n = m, n
    self.rows, self.cols = rows, cols
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

    With the four steps labeled:

    1. Column selection
    2. Row Selection
    3. Row reduction
    4. Variable elimination

    Returns a boolean:
      true if the pivot executed (continue iterating)
      false if optimal solution is found (stop algorithm)
    """
    # column selection
    best = 0
    pivot_j = -1
    for j in range(self.m + self.n):
      if self.tableau[0][j] < best:
        best = self.tableau[0][j]
        pivot_j = j
    if best == 0:  # halting condition
      return False
    # row selection
    best = float('inf')
    pivot_i = -1
    for i in range(1, self.m + 1):
      tmp = float(self.tableau[i][-1]) / self.tableau[i][pivot_j]
      if tmp < best:
        best = tmp
        pivot_i = i
    # row reduction
    pivot_el = self.tableau[pivot_i][pivot_j]
    self.tableau[pivot_i] = [
      (pivot_el ** -1.) * self.tableau[pivot_i][j]
      for j in range(self.cols)
    ]
    # variable elimination
    for i in range(self.rows):
      if i == pivot_i:
        continue
      el = float(self.tableau[i][pivot_j])
      if el == 0:
        continue
      self.tableau[i] = [
        self.tableau[i][j] - (el * self.tableau[pivot_i][j])
        for j in range(self.cols)
      ]
    return True


def simplex(c, A_ub, b_ub):
  """
  Simplex algorithm using the SimplexTableau class
  above.

  The algorithm finds the x such that

  dot(x, c)

  is maximized where

  A_ub * x <= b_ub

  where each b[i] is >= 0. The algorithm
  performs pivots using the process
  described above.

  This particular implementation assumes a
  solution to the linear program exists. A
  future improvement would be to add a test
  at some point that a solution to the system
  of inequalities exists.

  """
  tab = SimplexTableau(c, A_ub, b_ub)
  while tab.pivot_step():
    continue
  return tab.get_objective_metric()


if __name__ == '__main__':
  # Example from http://www.math.wsu.edu/faculty/dzhang/201/Guideline%20to%20Simplex%20Method.pdf
  # Correctly prints 12
  print simplex(
    (3, 1),
    (
      (2, 1),
      (2, 3),
    ),
    (8, 12),
  )
  # Example from https://en.wikipedia.org/wiki/Simplex_algorithm
  # Correctly prints 20
  print simplex(
    (2, 3, 4),
    (
      (3, 2, 1),
      (2, 5, 3),
    ),
    (10, 15),
  )
