"""
Median finding algorithm from lecture 2
---------------------------------------

"""


def select(S, i, key=lambda x: x):
  sublists = [S[k:k + 5] for k in range(0, len(S), 5)]
  medians = [
      sorted(sublist, key=key)[len(sublist) // 2]
      for sublist in sublists
  ]
  if len(medians) <= 5:
    x = medians[len(medians) // 2]
  else:
    x = select(medians, len(medians) // 2)
  L = [y for y in S if y < x]
  R = [y for y in S if y > x]
  k = len(L)
  if k > i:
    return select(L, i)
  if k < i:
    return select(R, i - k)
  return x
