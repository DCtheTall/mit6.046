"""
Lecture 23: Cache-Oblivious Algorithms
Strassen's Algorithm
--------------------
The lecture covers multiple matrix multiplication algorithms in the context
of cache-oblivious algorithms. Since (to my knowledge) it's not really possible
with Python to do actual cache-oblivious algorithms, doing a theoretical
model is really the best we can do.

So, given that scan.py contains such a model, this program will cover
the matrix multiplication algorithms covered in lecture: the naive
algorithm and then Strassen's divide-and-conquer algorithm.

"""


def check_valid_matrices(A, B):
  """
  Check if matrices are valid for multiplication.

  """
  mA, mB = len(A), len(B)
  if 0 in {mA, mB}:
    raise Exception('Empty matrix.')
  nA, nB = len(A[0]), len(B[0])
  if 0 in {nA, nB}:
    raise Exception('Empty matrix.')
  if mB != nA:
    raise Exception('Cannot multiply A and B.')


def pad_matrix(M):
  """
  Pad the matrix's dimensions to the smallest
  power of 2 greater than or equal to the number
  of rows and columns in the matrix.

  This eliminates edge cases for this example.

  """
  m, n = len(M), len(M[0])
  b = 1
  while b < max(m, n):
    b <<= 1
  M += [[0] * n for _ in range(b - m)]
  for i in range(b):
    M[i] += [0] * (b - n)
  return M


def split_matrix_quadrants(M):
  """
  Split the n x n matrix into 4 (n / 2) x (n / 2)
  matrices.

  """
  n = len(M) >> 1
  M11 = map(lambda row: row[:n], M[:n])
  M12 = map(lambda row: row[n:], M[:n])
  M21 = map(lambda row: row[:n], M[n:])
  M22 = map(lambda row: row[n:], M[n:])
  return M11, M12, M21, M22


def square_matrix_sum(A, B):
  """
  Sum two square matrices of equal
  size.

  """
  n = len(A)
  C = [[0] * n for _ in range(n)]
  for i in range(n):
    for j in range(n):
      C[i][j] = A[i][j] + B[i][j]
  return C


def square_matrix_subtract(A, B):
  """
  Subtract two square matrices of equal
  size.

  """
  n = len(A)
  C = [[0] * n for _ in range(n)]
  for i in range(n):
    for j in range(n):
      C[i][j] = A[i][j] - B[i][j]
  return C


def merge_quadrants(M11, M12, M21, M22):
  """
  Merge 4 quadrants of a matrix into a single
  list object. Recall that the + operator
  is list concatenation, not addition.

  """
  L = M11 + M21
  R = M12 + M22
  n = len(M11) << 1
  return [L[i] + R[i] for i in range(n)]


def naive_matrix_multiply(A, B):
  """
  Naive matrimx mulitplication algorithm.
  The algorithm traverses the matrix A by row
  and B by column and computes the dot product
  of the vectors. This is the standard way of
  multiplying matrices you see in math class.

  The complexity of this algorithm grows with the
  size of the sidelength of the matrices, n, on
  the order on O(n ** 3).

  """
  check_valid_matrices(A, B)
  A, B = pad_matrix(A), pad_matrix(B)
  n = len(A)
  if n == 1:
    return [[A[0][0] * B[0][0]]]
  A11, A12, A21, A22 = split_matrix_quadrants(A)
  B11, B12, B21, B22 = split_matrix_quadrants(B)
  C11 = square_matrix_sum(
    naive_matrix_multiply(A11, B11),
    naive_matrix_multiply(A12, B21),
  )
  C12 = square_matrix_sum(
    naive_matrix_multiply(A11, B12),
    naive_matrix_multiply(A12, B22),
  )
  C21 = square_matrix_sum(
    naive_matrix_multiply(A21, B11),
    naive_matrix_multiply(A22, B21),
  )
  C22 = square_matrix_sum(
    naive_matrix_multiply(A21, B12),
    naive_matrix_multiply(A22, B22),
  )
  return merge_quadrants(C11, C12, C21, C22)


def strassen_matrix_multiply(A, B):
  """
  Strassen's divide and conquer matrix multiplication
  algorithm.

  The complexity of this algorithm is better because
  it only takes 7 multiplications to compute the
  quadrants of the product, instead of 8 in the naive
  recursive algorithm.

  The complexity of this algorithm is O(n ** 2.8074). It
  is worth noting in both calculations we ignore the cost
  of adding matrix elements and only consider multiplication.

  """
  check_valid_matrices(A, B)
  A, B = pad_matrix(A), pad_matrix(B)
  n = len(A)
  if n == 1:
    return [[A[0][0] * B[0][0]]]
  A11, A12, A21, A22 = split_matrix_quadrants(A)
  B11, B12, B21, B22 = split_matrix_quadrants(B)
  M1 = strassen_matrix_multiply(
    square_matrix_sum(A11, A22),
    square_matrix_sum(B11, B22),
  )
  M2 = strassen_matrix_multiply(
    square_matrix_sum(A21, A22), B11)
  M3 = strassen_matrix_multiply(
    A11, square_matrix_subtract(B12, B22))
  M4 = strassen_matrix_multiply(
    A22, square_matrix_subtract(B21, B11))
  M5 = strassen_matrix_multiply(
    square_matrix_sum(A11, A12), B22)
  M6 = strassen_matrix_multiply(
    square_matrix_subtract(A21, A11),
    square_matrix_sum(B11, B12),
  )
  M7 = strassen_matrix_multiply(
    square_matrix_subtract(A11, A22),
    square_matrix_sum(B21, B22),
  )
  C11 = square_matrix_sum(
    square_matrix_subtract(
      square_matrix_sum(M1, M4),
      M5,
    ),
    M7,
  )
  C12 = square_matrix_sum(M3, M5)
  C21 = square_matrix_sum(M2, M4)
  C22 = square_matrix_sum(
    square_matrix_subtract(M1, M2),
    square_matrix_sum(M3, M6),
  )
  return merge_quadrants(C11, C12, C21, C22)
