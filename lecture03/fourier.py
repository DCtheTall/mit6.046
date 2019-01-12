"""
Lecture 3: Fast-Fourier Transform
---------------------------------
Topics covered:
- Recursion
- Divide and conquer

"""


import numpy as np
import math


def add(A, B):
  """
  Add two vetors (tuple of numbers)
  that represent polynomials as a
  coefficient

  if A = a_0 + x * a_1 + (x ** 2) * a_2 + ...
  and B = b_0 + x * b_1 + ...

  Then this function returns their sum
  expressed as a coefficient vector

  Complexity: O(n) where n is the highest degree term in the sum

  """
  n_A = len(A)
  n_B = len(B)
  n = max(n_A, n_B)
  C = [None for _ in range(n)]
  for i in range(n):
    c_i = 0
    if i < n_A:
      c_i += A[i]
    if i < n_B:
      c_i += B[i]
    C[i] = c_i
  return tuple(C)


def discrete_fourier_transform(A):
  """
  Recursive discrete Fourier transform on
  a polynomial, A, for this algorithm
  let's assume A has a length that
  is a power of 2

  Complexity: O(n * log(n))

  """
  n = len(A)
  if n == 1:
    return A
  omega = 1
  omega_n = np.exp(complex(0, 2 * math.pi / n))
  A_0 = []
  A_1 = []
  for i in range(n):
    if i % 2:
      A_1.append(A[i])
    else:
      A_0.append(A[i])
  A_0 = discrete_fourier_transform(A_0)
  A_1 = discrete_fourier_transform(A_1)
  A_hat = [0 for _ in range(n)]
  for i in range(n / 2):
    A_hat[i] = A_0[i] + (omega * A_1[i])
    A_hat[i + (n / 2)] = A_0[i] - (omega * A_1[i])
    omega *= omega_n
  return tuple(A_hat)


def inv_discrete_fourier_transform(A_hat):
  """
  Recursive inverse discrete Fourier transform on
  a transformed polynomial, A_hat

  Complexity: O(n * log(n))

  """
  m = len(A_hat)
  def recurse_inv_dft(L_hat):
    n = len(L_hat)
    if n == 1:
      return L_hat
    omega = 1
    omega_n = np.exp(complex(0, -2 * math.pi / n))
    L_0 = []
    L_1 = []
    for i in range(n):
      if i % 2:
        L_1.append(L_hat[i])
      else:
        L_0.append(L_hat[i])
    L_0 = recurse_inv_dft(L_0)
    L_1 = recurse_inv_dft(L_1)
    L = [0 for _ in range(n)]
    for i in range(n / 2):
      L[i] = L_0[i] + (omega * L_1[i])
      L[i + (n / 2)] = L_0[i] - (omega * L_1[i])
      omega *= omega_n
    return tuple(L)
  return tuple([float(a) / m for a in recurse_inv_dft(A_hat)])


def fast_polynomial_multiplication(A, B):
  """
  Fast polynomial multiplication which uses
  DFT, given a tuple of polynomial coefficients.
  This algorithm assumes the tuples have a length
  that is an even power of two

  Complexity: O(n * log(n))

  """
  if not A or not B: # Covers None and empty case
    return ()
  n_A = len(A)
  n_B = len(B)
  n = n_A + n_B
  A = [A[i] if i < n_A else 0 for i in range(n)]
  B = [B[i] if i < n_B else 0 for i in range(n)]
  C_star = [0 for _ in range(n)]
  A_star = discrete_fourier_transform(A)
  B_star = discrete_fourier_transform(B)
  for i in range(n):
    c_i = A_star[i]
    c_i *= B_star[i]
    C_star[i] = c_i
  return tuple(inv_discrete_fourier_transform(C_star))
