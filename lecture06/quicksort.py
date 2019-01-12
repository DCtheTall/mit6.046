"""
Lecture 6: Randomization
Quicksort
---------
Different implmentations of
quicksort

"""


from random import randint
from median import select


def basic_partition(L, lo, hi):
  """
  Partition function for a
  basic quicksort, just pick
  the highest index being
  considered

  """
  pivot = L[hi]
  i = lo - 1
  for k in range(lo, hi):
    if L[k] < pivot:
      i += 1
      L[i], L[k] = L[k], L[i]
  L[hi], L[i + 1] = L[i + 1], L[hi]
  return i + 1


def basic_quicksort(L, lo, hi):
  """
  Basic quicksort, has a worst-case
  complexity of O(n ** 2) for an
  already sorted array.

  To run this on the entire array,
  invoke with lo = 0 and hi = len(L) - 1

  """
  if lo < hi:
    pivot = basic_partition(L, lo, hi)
    basic_quicksort(L, lo, pivot - 1)
    basic_quicksort(L, pivot + 1, hi)

def linear_shuffle(L):
  """
  Random shuffling algorithm that runs
  in O(n) time

  """
  n = len(L)
  for i in range(n):
    k = i + (randint(0, n - 1) % (n - i))
    L[i], L[k] = L[k], L[i]


def basic_quicksort_with_shuffle(L):
  """
  Basic quicksort implementation with
  linear shuffle to help ensure
  we do not get the O(n ** 2) case

  """
  linear_shuffle(L)
  basic_quicksort(L, 0, len(L) - 1)


def intelligent_partition(L, lo, hi):
  """
  "Intelligent" partition by selecting
  the median as the pivot value using
  the O(n) algorithm from lecture 2

  """
  if hi == lo + 1:
    pivot = L[hi]
    i = hi
  else:
    pivot = select(L, (lo + hi) // 2)
    i = L.index(pivot)
  L[i], L[hi] = L[hi], L[i]
  pivot = L[hi]
  k = lo - 1
  for m in range(lo, hi):
    if L[m] < pivot:
      k += 1
      L[k], L[m] = L[m], L[k]
  L[hi], L[k + 1] = L[k + 1], L[hi]
  return k + 1


def intelligent_quicksort(L, lo, hi):
  """
  "Intelligent" quicksort partitions by finding
  the median on each recursion using the linear
  median finding algorithm. Due to the
  extra space and recursive calls needed, this
  does not perform better than mergesort
  in practice, even though it is guaranteed to
  be O(n * log(n))

  """
  if lo < hi:
    pivot = intelligent_partition(L, lo, hi)
    intelligent_quicksort(L, lo, pivot - 1)
    intelligent_quicksort(L, pivot + 1, hi)



def random_partition(L, lo, hi):
  """
  This implementation chooses a random element
  to be the pivot, and repeats until it tries
  either the resulting partitions are at least
  a quarter of the length of the list or
  it tried hi - lo times.

  """
  i = randint(lo, hi)
  L[i], L[hi] = L[hi], L[i]
  pivot = L[hi]
  k = lo - 1
  for m in range(lo, hi):
    if L[m] < pivot:
      k += 1
      L[k], L[m] = L[m], L[k]
  L[hi], L[k + 1] = L[k + 1], L[hi]
  n = len(L) // 4
  if (hi - lo > 4) \
    and (((i + 1) - lo) < n
      or (hi - (i + 1)) < n):
        return random_partition(L, lo, hi)
  return k + 1


def random_quicksort(L, lo, hi):
  """
  Randomized quicksort partitions on
  a randomly chosen pivot. To ensure
  that partitions are reasonably
  balanced, each partition will repeat
  until each side is at least a quarter
  the size of the whole part of the
  list that is being partitioned.

  """
  if lo < hi:
    pivot = random_partition(L, lo, hi)
    random_quicksort(L, lo, pivot - 1)
    random_quicksort(L, pivot + 1, hi)
