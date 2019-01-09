"""
Lecture 3: Divide and Conquer:
Order Statistics and Median Finding
-----------------------------------
This program shows a divide and conquer algorithm to
find the element of rank i in a list of elements S,
assuming the elements of S are unique.

"""


def select(S, i, key=lambda x: x):
  """
  Select the element, x of S with rank i (i elements in S < x)
  in linear time

  Assumes that the elements in S are unique

  Complexity: O(n)
  Every step in this algorithm is approximately linear
  time, the sorting here only ever happens of lists of
  length <= 5

  """
  # Divide the list into columns of 5
  sublists = [S[k:k+5] for k in range(0, len(S), 5)]
  # Find the medians of each column
  medians = [
    sorted(sublist, key=key)[len(sublist) // 2]
    for sublist in sublists
  ]
  if len(medians) <= 5:
    # If the number of columns is less than 5 elements
    # return the median of medians
    x = medians[len(medians) // 2]
  else:
    # Otherwise recursively find the median of medians
    x = select(medians, len(medians) // 2)
  L = [y for y in S if y < x]
  R = [y for y in S if y > x]
  k = len(L)
  if k > i:
    return select(L, i)
  if k < i:
    return select(R, i - k)
  return x



