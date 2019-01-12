"""
Lecture 6: Randomization
Frievalds' algorithm
--------------------
A randomized algorithm for verifying matrix multiplication.
Given three n * n matrices, A, B, and C, the algorithm verifies
that A * B = C

"""


from random import getrandbits


def generate_random_bit_vector(n):
  """
  Generates a random bit vector
  of length n

  """
  return [int(getrandbits(1)) for _ in range(n)]


def matrix_vector_multiply(M, v):
  """
  Multiply n * n matrix M with a
  n-dimensional vector v

  """
  return [
    sum([v[k] * m for k, m in enumerate(M[i])])
    for i in range(len(M))
  ]


def subtract_matrices(u, v):
  """
  Subtract two n-dimensional vectors

  """
  return sum([
    u[i] - v[i]
    for i in range(len(u))])


def freivalds(A, B, C, k=10):
  """
  Given 3 n * n matrices A, B, C
  verify that A * B = C
  in O(n ** 2) time with 1 / (2 ** k)
  probability of error

  This does so by generating a random
  bit vector r and verifying
  that A * (B * r) - (C * r) == 0
  k times

  """
  n = len(A)
  result = True
  for _ in range(k):
    r = generate_random_bit_vector(n)
    a = matrix_vector_multiply(A, r)
    b = matrix_vector_multiply(B, a)
    c = matrix_vector_multiply(C, r)
    result &= subtract_matrices(b, c) == 0
  return result
