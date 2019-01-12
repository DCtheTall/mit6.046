"""
Lecture 17: Approximation Algorithms
Set Cover
---------
Given a set X and a family of subsets S_1, S_2, ..., S_n,
find the smallest collection of subsets such that their
union is equal to all of X.

This program contains an approximation algorith which finds
a set cover by selecting the largest subset, then removing
all elements in this subset from X and all the other subsets.

This algorithm is a (1 + log(n))-approximation algorithm and
is not guaranteed to produce an optimal solution.

"""


def set_cover(X, subsets):
  """
  This algorithm finds an approximate solution
  to finding a minimum collection of subsets
  that cover the set X.

  It is shown in lecture that this is a
  (1 + log(n))-approximation algorithm.

  """
  cover = set()
  subsets_copy = list(subsets)
  while True:
    S = max(subsets_copy, key=len)
    if len(S) == 0:
      break
    cover.add(subsets.index(S))
    subsets_copy.pop(subsets_copy.index(S))
    for x in S:
      for T in subsets_copy:
        if x in set(T):
          T.remove(x)
  return cover


if __name__ == '__main__':
  """
  Below is an implementation of the example of
  set cover in lecture 17

  """
  X = {i for i in range(12)}
  subsets = [
    {i for i in range(6)},
    {4, 5, 7, 8},
    {3 * i for i in range(4)},
    {9, 10},
    {(3 * i) + 2 for i in range(4)},
    {1, 4, 6, 7, 10},
  ]
  print set_cover(X, subsets)
