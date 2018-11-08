"""
Linear Programming
------------------
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


if __name__ == '__main__':
  """
  Below is a basic implementation of scipy.optimize's linprog
  function being used to solve the example in lecture.

  Since the lecture gave the constraints as lower bounds
  and scipy uses upper bounds, I had to negate the
  constraining inequalities.

  Run the program to see the result!

  """
  c = (1, 1, 1, 1)
  A_ub = \
    ((2, -8, 0, -10),
     (-5, -2, 0, 0),
     (-3, 5, -10, -2))
  b_ub = (-500000, -100000, -25000)
  x = linprog(c, A_ub, b_ub, method='interior-point')
  print x
