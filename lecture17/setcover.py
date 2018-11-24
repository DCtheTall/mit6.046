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
  while True:
    S = max(subsets, key=len)
    if len(S) == 0:
      break
    cover.add(subsets.index(S))
    for x in S:
      for T in subsets:
        if x in T:
          T.remove(x)
  return cover
