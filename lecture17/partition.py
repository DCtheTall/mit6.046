"""
Lecture 17: Approximation Algorithms
Set Partition
-------------
Given a subset of the real numbers S, a partition is
a collection of disjoint subsets whose union
is all of S.

The goal of this program is to find a partition
of S made up of two subsets, A and B, that minimizes
the quantity:

max(sum(x for x in A), sum(x for x in B))

i.e. the partition of S, A and B, such that the sum
of the elements in each subset are as close as
possible. This program contains two approaches:

The first is a brute force approach which computes
the power set of S and then looks at all possible
partitions of S to find the optimal solution.

"""


def brute_force_partition(S):
  """
  Brute force partition algorithm

  This function finds the optimal partition of the
  subset of the real numbers, S, by computing every
  possible subset of S and comparing every possible
  partition for the optimal one.

  This algorithm takes exponential time, since
  computing the power set takes exponential time.

  """
  power_set = [set()]
  for x in S:
    for A in list(power_set):
      power_set.append(A.union({x}))
  partition = (S, set())
  best = sum(S)
  for A in power_set:
    B = S.difference(A)
    val = max(sum(A), sum(B))
    if val < best:
      partition = (A, B)
      best = val
  return partition
